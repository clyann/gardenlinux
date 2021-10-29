#!/usr/bin/env python3

import argparse
import dataclasses
import paths
from glci.model import BuildType
from glci.model import PublishingAction

import render_pipeline_run as renderer

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--committish',
        help='commit of release canditate'
        )
    parser.add_argument(
        '--branch',
        default='main',
        help='branch to build rc from (default: main)'
    )
    parser.add_argument(
        '--gardenlinux-epoch',
        help='the gardenlinux epoch of the release-candidate',
    )
    parser.add_argument(
        '--outfile',
        default='release-from-rc-run.yaml',
        help='name of rendered pipeline-run yaml',
    )
    parser.add_argument('--disable-notifications', action='store_const', const=True, default=False)
    parser.add_argument('--additional-recipients', default=' ')
    parser.add_argument('--only-recipients', default=' ')

    publishing_actions = (
        PublishingAction.MANIFESTS,
        PublishingAction.IMAGES,
        PublishingAction.RELEASE_CANDIDATE,
        PublishingAction.RELEASE,
        PublishingAction.COMPONENT_DESCRIPTOR,
    )
    parsed = parser.parse_args()

    setattr(parsed, 'cicd_cfg', 'default')
    setattr(parsed, 'pipeline_cfg', paths.flavour_cfg_path)
    setattr(parsed, 'oci_path', 'eu.gcr.io/gardener-project/gardenlinux')
    setattr(parsed, 'flavour_set', 'all')
    setattr(parsed, 'git_url', 'https://github.com/gardenlinux/gardenlinux.git')
    setattr(parsed, 'publishing_actions', publishing_actions)
    setattr(parsed, 'version',f'{parsed.gardenlinux_epoch}.0')
    setattr(parsed, 'pytest_cfg','default')
    setattr(parsed, 'promote_target', BuildType.RELEASE)

    print(f'{parsed=}')
    pipeline_run = renderer.mk_pipeline_main_run(
        args=parsed,
    )

    pipeline_run_dict = dataclasses.asdict(pipeline_run)

    with open(parsed.outfile, 'w') as f:
        yaml.safe_dump(pipeline_run_dict, f)

    print(f'pipeline-run written to {parsed.outfile}')


if __name__ == '__main__':
    main()
