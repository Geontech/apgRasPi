# RPM package for gps_node
# This file is regularly AUTO-GENERATED by the IDE. DO NOT MODIFY.

# By default, the RPM will install to the standard REDHAWK SDR root location (/var/redhawk/sdr)
# You can override this at install time using --prefix /new/sdr/root when invoking rpm (preferred method, if you must)
%{!?_sdrroot: %define _sdrroot /var/redhawk/sdr}
%define _prefix %{_sdrroot}
Prefix: %{_prefix}

Name: gps_node
Summary: Node gps_node
Version: 1.0.0
Release: 1
License: None
Group: REDHAWK/Nodes
Source: %{name}-%{version}.tar.gz
# Require the device manager whose SPD is referenced
Requires: DeviceManager
# Require each referenced device/service
Requires: gps_receiver GPP
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

%description

%prep
%setup

%install
%__rm -rf $RPM_BUILD_ROOT
%__mkdir_p "$RPM_BUILD_ROOT%{_prefix}/dev/nodes/%{name}"
%__install -m 644 DeviceManager.dcd.xml $RPM_BUILD_ROOT%{_prefix}/dev/nodes/%{name}/DeviceManager.dcd.xml

%files
%defattr(-,redhawk,redhawk)
%dir %{_prefix}/dev/nodes/%{name}
%{_prefix}/dev/nodes/%{name}/DeviceManager.dcd.xml
