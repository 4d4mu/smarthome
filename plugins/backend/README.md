# Backend GUI

This plugin delivers information about the current SmarthomeNG installation. Right now it serves as a support tool for helping other users with an installation that does not run properly. Some highlights:

* a list of installed python modules is shown versus the available versions from PyPI
* a list of items and their attributes is shown
* a list of logics and their next execution time
* a list of current schedulers and their next execution time
* direct download of sqlite database (if plugin is used) and smarthome.log
* some information about frequently used daemons like knxd is included
* supports basic authentication
* multi-language support

There is however only basic protection against unauthorized access or use of the plugin so be careful when enabling it with your network.

It is still in early development so please give feedback to the community.

# Requirements
This plugin requires Python >= 3.4 as well as the libs cherrypy and jinja2. You can install them with:
<pre>
(sudo apt-get install python-cherrypy)
sudo pip3 install cherrypy
(sudo apt-get install python-jinja2)
sudo pip3 install jinja2
</pre>
And please pay attention that the libs are installed for Python3 and not an older Python 2.7 that is probably installed on your system.

## Running this plugin under Python 3.2
If you really need to run this plugin under Python 3.2 you may not use the newest version of all packages. Make sure to install the following versions into your Phython3.2 environment, as newer versions are not compatible with Python 3.2 any more:

<pre>
- Jinja2	v2.6
- MarkupSafe	v0.15
</pre>

.

To support visualization, the visu_websocket plugin has to be used. It has to be PLUGIN_VERSION >= "1.1.2".


# Configuration

## plugin.conf
<pre>
[BackendServer]
	class_name = BackendServer
	class_path = plugins.backend
	#ip = xxx.xxx.xxx.xxx
	#port = 8383
	#updates_allowed = True
	#user = admin
	#password = very_secure_password
	#language = en
</pre>

### ip
IP address to start the backend server. Usually it doesnot need to be configured.

If not configured the standard ip address of the system is used. If you like to restrict the usage of the BackendServer to the system itself (the browser ist running on the smarthomeNG system itself), you can configure the ip to 127.0.0.1. In this case, the BackendServer is only available through the localhost address.

### port
The port on which the backend server listens. By default port **`8383`** is used.

###    updates_allowed

By default, the backend server allows updates to the running smarthomeNG instance. For instance, it is possible to trigger or to reload a logic. Setting **`updates_allowed`** to **`False`**, you can disable these features.

### user (optional)
The user for basic authentication. If left out, the user name is set as "admin"

### password (optional)
The password for basic authentication. If left out, basic authentication is disabled.

### language (optional)
You can specify a language to use for the plugin. Besides the standard language (german) which is used, if this parameter isn't set, you can specify english (for the time being). The language is specified by  **`en`**