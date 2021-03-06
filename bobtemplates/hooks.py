# -*- coding: utf-8 -*-

from datetime import date
import os
import shutil
import ConfigParser


def pre_url(configurator, question):
    """
    Construct url from previous question
    """
    hoster = configurator.variables.get('git.hoster')
    package_name = configurator.variables.get('package.dottedname')
    if hoster == 'Github':
        url = 'https://github.com/affinitic/%s'
    elif hoster == 'Gitlab':
        url = 'http://git.affinitic.be/clients/%s'
    question.default = url % package_name


def prepare_render(configurator):
    """Some variables to make templating easier.

    This is especially important for allowing nested and normal packages.
    """
    # get package-name and package-type from user-input
    configurator.variables['year'] = date.today().year
    package_dir = os.path.basename(configurator.target_directory)
    nested = bool(len(package_dir.split('.')) == 3)
    configurator.variables['package.nested'] = nested
    configurator.variables['package.namespace'] = package_dir.split('.')[0]
    if nested:
        namespace2 = package_dir.split('.')[1]
    else:
        namespace2 = None
    configurator.variables['package.namespace2'] = namespace2
    configurator.variables['package.name'] = package_dir.split('.')[-1]

    if nested:
        dottedname = "{0}.{1}.{2}".format(
            configurator.variables['package.namespace'],
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'])
    else:
        dottedname = "{0}.{1}".format(
            configurator.variables['package.namespace'],
            configurator.variables['package.name'])

    # package.dottedname = 'collective.foo.something'
    configurator.variables['package.dottedname'] = dottedname

    # package.slashname = 'collective/foo/something'
    configurator.variables['package.slashname'] = dottedname.replace('.', '/')

    # package.uppercasename = 'COLLECTIVE_FOO_SOMETHING'
    configurator.variables['package.uppercasename'] = configurator.variables[
        'package.dottedname'
    ].replace('.', '_').upper()

    camelcasename = dottedname.replace('.', ' ').title()\
        .replace(' ', '')\
        .replace('_', '')
    browserlayer = "{0}Layer".format(camelcasename)

    # package.browserlayer = 'CollectiveFooSomethingLayer'
    configurator.variables['package.browserlayer'] = browserlayer

    # package.longname = 'collectivefoosomething'
    configurator.variables['package.longname'] = camelcasename.lower()

    # jenkins.directories = 'collective/foo/something'
    configurator.variables['jenkins.directories'] = dottedname.replace('.', '/')  # NOQA: E501

    # namespace_packages = "['collective', 'collective.foo']"
    if nested:
        namespace_packages = "'{0}', '{0}.{1}'".format(
            configurator.variables['package.namespace'],
            configurator.variables['package.namespace2'])
    else:
        namespace_packages = "'{0}'".format(
            configurator.variables['package.namespace'])
    configurator.variables['package.namespace_packages'] = namespace_packages

    if configurator.variables.get('theme.name'):
        def normalize_string(value):
            value = '-'.join(value.split('_'))
            value = '-'.join(value.split())
            return value
        configurator.variables['theme.normalized_name'] = normalize_string(
            configurator.variables.get('theme.name'),
        ).lower()
    else:
        configurator.variables['theme.normalized_name'] = ''


def cleanup_package(configurator):
    """Cleanup and make nested if needed.

    Transform into a nested package if that was the selected option.
    Remove parts that are not needed depending on the chosen configuration.
    """

    nested = configurator.variables['package.nested']

    # construct full path '.../src/collective'
    start_path = "{0}/src/{1}".format(
        configurator.target_directory,
        configurator.variables['package.namespace'])

    # path for normal packages: '.../src/collective/myaddon'
    base_path = "{0}/{1}".format(
        start_path,
        configurator.variables['package.name'])

    if nested:
        # Event though the target-dir was 'collective.behavior.myaddon' mrbob
        # created a package collective.behavior.myaddon/src/collective/myaddon
        # since the template does not hava a folder for namespace2.
        # Here this package is turned into a nested package
        # collective.behavior.myaddon/src/collective/behavior/myaddon by
        # inserting a folder with the namepsace2 ('behavior') and oopying
        # a __init__.py into it.

        # full path for nested packages: '.../src/collective/behavior/myaddon'
        base_path_nested = "{0}/{1}/{2}".format(
            start_path,
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'])

        # directory to be created: .../src/collective/behavior
        newpath = "{0}/{1}".format(
            start_path,
            configurator.variables['package.namespace2'])
        if not os.path.exists(newpath):
            # create new directory .../src/collective/behavior
            os.makedirs(newpath)

        # copy .../src/collective/__init__.py to
        # .../src/collective/myaddon/__init__.py
        shutil.copy2("{0}/__init__.py".format(start_path), newpath)

        # move .../src/collective/myaddon to .../src/collective/behavior
        shutil.move(base_path, base_path_nested)


def post_render(configurator):
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    settings = configurator.target_directory + '/settings.cfg'
    config.read(settings)
    config.set('settings', 'package_policy', configurator.variables['policy.name'])
    config.set('settings', 'package_core', configurator.variables['core.name'])
    config.set('settings', 'package_theme', configurator.variables['theme.name'])
    with open(settings, 'w') as configfile:
        config.write(configfile)

    sources = configurator.target_directory + '/sources.cfg'

    file = open(sources, 'rb').read()
    lines = file.split("\n")
    result = []
    for line in lines:
        var = line.replace('package_policy_source_name', configurator.variables['policy.name']).replace('package_core_source_name', configurator.variables['core.name']).replace('package_theme_source_name', configurator.variables['theme.name'])
        result.append(var)
    open(sources, 'wb').write("\n".join(result))
