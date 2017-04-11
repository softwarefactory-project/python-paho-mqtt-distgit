%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global scrname paho-mqtt

Name:           python-paho-mqtt
Version:        1.1
Release:        1%{?dist}
Summary:        A Python MQTT version 3.1/3.1.1 client class

License:        EPL
URL:            http://eclipse.org/paho/
Source0:        https://pypi.python.org/packages/source/p/%{scrname}/%{scrname}-%{version}.tar.gz
Buildarch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
This library provides a client class which enable applications to connect to
an MQTT broker to publish messages, and to subscribe to topics and receive
published messages. It also provides some helper functions to make publishing
one off messages to an MQTT server very straightforward.

The MQTT protocol is a machine-to-machine (M2M) connectivity protocol. Designed
as an extremely lightweight publish/subscribe messaging transport, it is useful
for connections with remote locations where a small code footprint is required
and/or network bandwidth is at a premium.

%if 0%{?with_python3}
%package -n python3-paho-mqtt
Summary:        A Python MQTT version 3.1/3.1.1 client class

Requires:       python3
BuildArch:      noarch

%description -n python3-paho-mqtt
This library provides a client class which enable applications to connect to
an MQTT broker to publish messages, and to subscribe to topics and receive
published messages. It also provides some helper functions to make publishing
one off messages to an MQTT server very straightforward.

The MQTT protocol is a machine-to-machine (M2M) connectivity protocol. Designed
as an extremely lightweight publish/subscribe messaging transport, it is useful
for connections with remote locations where a small code footprint is required
and/or network bandwidth is at a premium.
%endif

%prep
%setup -q -n %{scrname}-%{version}
 sed -i "s|\r||g" CONTRIBUTING.md
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%doc CONTRIBUTING.md LICENSE.txt README.rst *.html
%{python2_sitelib}/paho/
%{python2_sitelib}/paho*.egg-info

%if 0%{?with_python3}
%files -n python3-paho-mqtt
%doc CONTRIBUTING.md LICENSE.txt README.rst *.html
%{python3_sitelib}/paho/
%{python3_sitelib}/paho*.egg-info
%endif # with_python3

%changelog
* Thu Feb 05 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1.1-1
- Update to new upstream version 1.1

* Wed Aug 20 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1.0-1
- Initial package
