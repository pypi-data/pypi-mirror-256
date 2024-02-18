# copyright ############################### #
# This file is part of the Xcoll Package.   #
# Copyright (c) CERN, 2023.                 #
# ######################################### #

import numpy as np
import pandas as pd

import xobjects as xo
import xpart as xp
import xtrack as xt


def install_black_absorbers(self, names=None, *, verbose=False):
    if names is None:
        names = self.collimator_names
    def install_func(thiscoll, name):
        return BlackAbsorber(
                inactive_front=thiscoll['inactive_front'],
                inactive_back=thiscoll['inactive_back'],
                active_length=thiscoll['active_length'],
                angle=[thiscoll['angle_L'],thiscoll['angle_R']],
                active=False,
                _tracking=False,
                _buffer=self._buffer
               )
    self._install_collimators(names, install_func=install_func, verbose=verbose)


def install_everest_collimators(self, names=None, *, verbose=False):
    if names is None:
        names = self.collimator_names
    df = self.colldb._colldb.loc[names]
    df_coll = df[[c is None for c in df.crystal]]
    df_cry  = df[[c is not None for c in df.crystal]]
    # Do the installations
    if len(df_coll) > 0:
        def install_func(thiscoll, name):
            return EverestCollimator(
                    inactive_front=thiscoll['inactive_front'],
                    inactive_back=thiscoll['inactive_back'],
                    active_length=thiscoll['active_length'],
                    angle=[thiscoll['angle_L'],thiscoll['angle_R']],
                    material=SixTrack_to_xcoll[thiscoll['material']][0],
                    active=False,
                    _tracking=False,
                    _buffer=self._buffer
                   )
        self._install_collimators(df_coll.index.values, install_func=install_func, verbose=verbose)
    if len(df_cry) > 0:
        def install_func(thiscoll, name):
            material = SixTrack_to_xcoll[thiscoll['material']]
            if len(material) < 2:
                raise ValueError(f"Could not find crystal material definition from variable {thiscoll['material']}!")
            material = material[1]
            if not isinstance(material, CrystalMaterial):
                raise ValueError(f"The material {material.name} is not a Crystalmaterial!")
            return EverestCrystal(
                    inactive_front=thiscoll['inactive_front'],
                    inactive_back=thiscoll['inactive_back'],
                    active_length=thiscoll['active_length'],
                    angle=[thiscoll['angle_L'],thiscoll['angle_R']],
                    material=material,
                    active=False,
                    _tracking=False,
                    _buffer=self._buffer
                   )
        self._install_collimators(df_cry.index.values, install_func=install_func, verbose=verbose)


def _install_collimators(self, names, *, install_func, verbose, support_legacy_elements=False):
    # Check that collimator marker exists in Line and CollimatorDatabase,
    # and that tracker is not yet built
    # TODO: need check that all collimators have aperture before and after
    line = self.line
    df = self.colldb._colldb
    mask = df.index.isin(names)
    for name in names:
        if name not in line.element_names:
            raise Exception(f"Collimator {name} not found in line!")
        elif name not in self.collimator_names:
            raise Exception(f"Warning: Collimator {name} not found in CollimatorDatabase!...")
    if self.tracker_ready:
        raise Exception("Tracker already built!\nPlease install collimators before building tracker!")

    # Loop over collimators to install
    for name in names:

        # Get the settings from the CollimatorDatabase
        thiscoll = df.loc[name]
        # Create the collimator element
        newcoll = install_func(thiscoll, name)
        collimator_class = newcoll.__class__

        # Check that collimator is not installed as different type
        # TODO: automatically replace collimator type and print warning
        if isinstance(line[name], tuple(_all_collimator_types - {collimator_class})):
            raise ValueError(f"Trying to install {name} as {collimator_class.__name__},"
                             + f" but it is already installed as {type(line[name]).__name__}!\n"
                             + "Please reconstruct the line.")

        # Check that collimator is not installed previously
        elif isinstance(line[name], collimator_class):
            if df.loc[name,'collimator_type'] != collimator_class.__name__:
                raise Exception(f"Something is wrong: Collimator {name} already installed in line "
                                + f"as {collimator_class.__name__} element, but registered in CollimatorDatabase "
                                + f"as {df.loc[name, 'collimator_type']}. Please reconstruct the line.")
            if verbose: print(f"Collimator {name} already installed. Skipping...")
            continue

        # TODO: only allow Marker elements, no Drifts!!
        #       How to do this with importing a line for MAD-X or SixTrack...?
        elif not isinstance(line[name], (xt.Marker, xt.Drift)) and not support_legacy_elements:
            raise ValueError(f"Trying to install {name} as {collimator_class.__name__},"
                             + f" but the line element to replace is not an xtrack.Marker (or xtrack.Drift)!\n"
                             + "Please check the name, or correct the element.")

        if verbose: print(f"Installing {name:20} as {collimator_class.__name__}")

        # Update the position and type in the CollimatorDatabase
        ss = line.get_s_position()
        idx = line.element_names.index(name)
        df.loc[name,'s_center'] = ss[idx]
        df.loc[name,'collimator_type'] = collimator_class.__name__

        # Find apertures       TODO same with cryotanks for FLUKA   TODO: use compound info  ->  need full collimator info from MADX
        aper_before = {}
        aper_after = {}
        if f'{name}_mken' in line.element_names\
        and f'{name}_mkex'in line.element_names:
            # TODO what with transformations? How to shift them in s if different?
            aper_before = {nn.replace('mken', 'upstream'): line[nn].copy()
                           for nn in line.element_names if nn.startswith(f'{name}_mken_aper')}
            aper_after  = {nn.replace('mkex', 'downstream'): line[nn].copy()
                           for nn in line.element_names if nn.startswith(f'{name}_mkex_aper')}
        if len(aper_before) == 0:
            # TODO what with transformations? How to shift them in s from centre to start/end?
            aper_before = {nn.replace('_aper', '_upstream_aper'): line[nn].copy()
                           for nn in line.element_names if nn.startswith(f'{name}_aper')}
        if len(aper_after) == 0:
            aper_after  = {nn.replace('_aper', '_downstream_aper'): line[nn].copy()
                           for nn in line.element_names if nn.startswith(f'{name}_aper')}

        # Remove stuff at location of collimator
        l = thiscoll['active_length']
        to_remove = []
        i = idx - 1
        # We remove everything between the beginning and end of the collimator except drifts
        while ss[i] >= ss[idx] - l/2:
            el = line[i]
            if el.__class__.__name__ == 'Drift':
                i -= 1
                continue
            nn = line.element_names[i]
            if hasattr(el, 'length') and el.length > 0:
                raise ValueError(f"Found active element with length {el.length} at location inside collimator!")
            to_remove.append(nn)
            i -= 1
        i = idx + 1
        while ss[i] <= ss[idx] + l/2:
            el = line[i]
            if el.__class__.__name__ == 'Drift':
                i += 1
                continue
            nn = line.element_names[i]
            if hasattr(el, 'length') and el.length > 0:
                raise ValueError(f"Found active element with length {el.length} at location inside collimator!")
            to_remove.append(nn)
            i += 1
        for nn in to_remove:
            # TODO: need to update Compounds
            line.element_names.remove(nn)
            line.element_dict.pop(nn)

        # Do the installation
        s_install = df.loc[name,'s_center'] - thiscoll['active_length']/2 - thiscoll['inactive_front']
        line.insert_element(element=newcoll, name=name, at_s=s_install)

        # Install apertures
        for aper in aper_before.keys():
            # TODO: need to update Compounds
            line.insert_element(element=aper_before[aper], name=aper, index=name)
        for aper in list(aper_after.keys())[::-1]:
            # TODO: need to update Compounds
            line.insert_element(element=aper_after[aper], name=aper,
                                index=line.element_names.index(name)+1)