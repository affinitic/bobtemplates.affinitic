#!/bin/sh
buildout() { read -p "please provide name of buildout " $1 ; }
policy() { read -p "please provide name of policy package " $1 ; }
core() { read -p "please provide name of core package " $1 ; }
theme() { read -p "please provide name of theme package " $1 ; }

buildout buildout_name
core core_name
policy policy_name
theme theme_name

bin/mrbob -O $buildout_name bobtemplates.affinitic:complete_plone5_buildout
bin/mrbob -O $core_name bobtemplates.plone:addon
bin/mrbob -O $policy_name bobtemplates.plone:addon
bin/mrbob -O $theme_name bobtemplates.plone:addon

python run.py --policy=$policy_name --core=$core_name --theme=$theme_name