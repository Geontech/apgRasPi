# RPM package for waveform_example
# This file is regularly AUTO-GENERATED by the IDE. DO NOT MODIFY.

# By default, the RPM will install to the standard REDHAWK SDR root location (/var/redhawk/sdr)
# You can override this at install time using --prefix /new/sdr/root when invoking rpm (preferred method, if you must)
%{!?_sdrroot: %define _sdrroot /var/redhawk/sdr}
%define _prefix %{_sdrroot}
Prefix: %{_prefix}

Name: waveform_example
Summary: Waveform waveform_example
Version: 1.0.0
Release: 1
License: None
Group: REDHAWK/Waveforms
Source: %{name}-%{version}.tar.gz
# Require the controller whose SPD is referenced
Requires: DataConverter
# Require each referenced component
Requires: DataConverter TuneFilterDecimate AmFmPmBasebandDemod
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
An example waveform for the APG Tech Challenge Raspberry Pi + USB RTL node.

%prep
%setup

%install
%__rm -rf $RPM_BUILD_ROOT
%__mkdir_p "$RPM_BUILD_ROOT%{_prefix}/dom/waveforms/%{name}"
%__install -m 644 waveform_example.sad.xml $RPM_BUILD_ROOT%{_prefix}/dom/waveforms/%{name}/waveform_example.sad.xml

%files
%defattr(-,redhawk,redhawk)
%dir %{_prefix}/dom/waveforms/%{name}
%{_prefix}/dom/waveforms/%{name}/waveform_example.sad.xml