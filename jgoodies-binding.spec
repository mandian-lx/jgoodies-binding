%{?_javapackages_macros:%_javapackages_macros}

%define oname JGoodies
%define shortoname Binding
%define releasedate 20150121

%define bname %(echo %oname | tr [:upper:] [:lower:])
%define shortname %(echo %shortoname | tr [:upper:] [:lower:])

%define version 2.13.0
%define oversion %(echo %version | tr \. _)

Summary:	Swing Data Binding Framework
Name:		%{bname}-%{shortname}
Version:	%{version}
Release:	1
License:	BSD
Group:		Development/Java
URL:		http://www.jgoodies.com/freeware/libraries/%{shortname}/
Source0:	http://www.jgoodies.com/download/libraries/%{shortname}/%{name}-%{oversion}-%{releasedate}.zip
# NOTE: Latest version of jgoodies libraries can't be freely download from
#	from the official site. However official maven repo provides some
#	more updated versions
# Source0:	https://repo1.maven.org/maven2/com/%{bname}/%{name}/%{version}/%{name}-%{version}-sources.jar
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(com.jgoodies:jgoodies-common)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:	fontconfig
BuildRequires:	fonts-ttf-dejavu

%description
The JGoodies Binding synchronizes object properties with Swing components.
And it helps you represent the state and behavior of a presentation
independently of the GUI components used in the interface.

The JGoodies Binding requires Java 6 or later.

%files -f .mfiles
%doc README.html
%doc RELEASE-NOTES.txt
%doc LICENSE.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{oname} %{shortoname}
Requires:	jpackage-utils

%description javadoc
API documentation for %{oname} %{shortoname}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q
# Extract sources
mkdir -p src/main/java/
pushd src/main/java/
%jar -xf ../../../%{name}-%{version}-sources.jar
popd

# Extract tests
mkdir -p src/test/java/
pushd src/test/java/
%jar -xf ../../../%{name}-%{version}-tests.jar
popd

# Delete prebuild JARs and binaries and docs
find . -name "*.jar" -delete
find . -name "*.class" -delete
rm -fr docs

# Add an OSGi compilant MANIFEST.MF
%pom_add_plugin org.apache.felix:maven-bundle-plugin . "
<extensions>true</extensions>
<configuration>
	<supportedProjectTypes>
		<supportedProjectType>bundle</supportedProjectType>
		<supportedProjectType>jar</supportedProjectType>
	</supportedProjectTypes>
	<instructions>
		<Bundle-Name>\${project.artifactId}</Bundle-Name>
		<Bundle-Version>\${project.version}</Bundle-Version>
	</instructions>
</configuration>
<executions>
	<execution>
		<id>bundle-manifest</id>
		<phase>process-classes</phase>
		<goals>
			<goal>manifest</goal>
		</goals>
	</execution>
</executions>"

# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build

%install
%mvn_install

