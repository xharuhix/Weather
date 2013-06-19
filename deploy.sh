#!/bin/bash

function check_uid()
{
	if [ $EUID -ne 0 ]; then
  	echo "root 権限で実行してください"
		return 1
	fi
}

function deploy()
{
	check_uid || return

	# install required packages...
	if ! rpm -q python-setuptools >/dev/null 2>&1; then
		yum -y install python-setuptools
	fi
	
	# install pip
	easy_install pip

	# install virtualenv
	pip install virtualenv
}


function virtdeploy()
{
	# create vitual enviroment
	virtualenv  --no-site-package .

	# enter vitual enviroment
	source ./bin/activate

}

function clean()
{
	# clean
	rm -rf ./bin
	rm -rf ./include
	rm -rf ./lib
	rm -rf ./lib64
}

function usage()
{
	cat <<EOF
Usage:
	# デプロイ
	sudo ./stiercmd deploy
	sudo ./stiercmd virtdeploy
EOF
}

case "$1" in
	"clean") clean $@;;
	"deploy") deploy $@;;
	"virtdeploy") virtdeploy $@;;
	*) usage;;
esac

# vim: set nu ts=2 autoindent : 
