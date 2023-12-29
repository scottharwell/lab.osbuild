=========================
Lab.Osbuild Release Notes
=========================

.. contents:: Topics


v1.1.5
======

Release Summary
---------------

Minor bug fixes

Minor Changes
-------------

- Continued rhel version abstraction work.
- Updated hard-coded architectures.

v1.1.4
======

Release Summary
---------------

Role portability improvements.

Minor Changes
-------------

- Added EPEL repo to build blueprints.
- Broke osbuild configuration into multiple tasks for portability.
- Remove unneeded assert.
- Removed conditional variables that became redundant with new task files.
- Updated build command for AWS key format.

v1.1.3
======

Release Summary
---------------

Added the size flag to the composer build command.

Minor Changes
-------------

- Added the size flag to the composer build command and set the default size to 4096.

v1.1.2
======

Release Summary
---------------

Cleanup repo_info module

Minor Changes
-------------

- Remove SSH key from root user.
- Updates to the code base of the repo_info module.

New Modules
-----------

- lab.osbuild.gpg_file_info - Retrieves GPG keys from files on Linux systems.

v1.1.1
======

Release Summary
---------------

Converted python scripts to Ansible modules.

Major Changes
-------------

- Converted python scripts to Ansible modules.

New Modules
-----------

- lab.osbuild.repo_info - Retrieves information about repositories managed by subscription manager.

v1.1.0
======

Release Summary
---------------

Added AWS build blueprint

Major Changes
-------------

- Added AWS image build capabilities.
- Added AWS setup role.
- Added Azure setup role.

Breaking Changes / Porting Guide
--------------------------------

- Changed file names to align with conventions in osbuilder documentation.
- Removed variables that were specific to Azure or replaced with cloud naming conventions.

v1.0.2
======

Release Summary
---------------

Bug fixes

Minor Changes
-------------

- Updated use of `shell` command to `copy` and `cmd` since the shell command does not report on stderror.

v1.0.1
======

Release Summary
---------------

Update repository removing unused variables and README cleanup.

Major Changes
-------------

- Renamed `setup_host` role to `host_setup` to match naming conventions.

Minor Changes
-------------

- Added mdlint file.
- Changed hosts to be "all" instead of "rhel-dev".
- README updates.

v1.0.0
======

Release Summary
---------------

Created collection of roles for osbuild deployment.

Major Changes
-------------

- Migrated repository to collection layout with roles.
- Resolved ansible-lint issues.
