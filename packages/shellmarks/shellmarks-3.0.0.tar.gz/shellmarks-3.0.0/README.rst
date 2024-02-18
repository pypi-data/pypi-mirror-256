.. image:: http://img.shields.io/pypi/v/shellmarks.svg
    :target: https://pypi.org/project/shellmarks
    :alt: This package on the Python Package Index

.. image:: https://github.com/Josef-Friedrich/ansible-module-shellmarks/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/ansible-module-shellmarks/actions/workflows/tests.yml
    :alt: Tests

ansible-module-shellmarks
=========================

``ansible-module-shellmarks`` is a `ansible <https://www.ansible.com>`_
module to set bookmarks to commonly used directories like the tools
`shellmarks <https://github.com/Bilalh/shellmarks>`_ /
`bashmarks <https://github.com/huyng/bashmarks>`_ do.

`shellmarks <https://github.com/Bilalh/shellmarks>`_ and
`bashmarks <https://github.com/huyng/bashmarks>`_ are shell scripts
that allows you to save and jump to commonly used directories with tab
completion.

Both tools store their bookmarks in a text file called ``~/.sdirs``.
This module is able to write bookmarks to this file.

::

   export DIR_shell_scripts_SHELL_GITHUB="$HOME/shell-scripts"
   export DIR_shellmarks_module_ansible="$HOME/ansible-module-shellmarks"
   export DIR_skeleton_SHELL_GITHUB="$HOME/skeleton.sh"

.. code-block:: 

    > SHELLMARKS    (/etc/ansible/library/shellmarks.py)

            shellmarks https://github.com/Bilalh/shellmarks bashmarks
            https://github.com/huyng/bashmarks are shell scripts that
            allows you to save and jump to commonly used directories with
            tab completion.

    OPTIONS (= is mandatory):

    - cleanup
            Delete bookmarks of nonexistent directories.
            default: false

    - delete_duplicates
            Delete duplicate bookmark entries. This option deletes both
            duplicate mark and duplicate path entries. Entries at the
            beginning are deleted, entries at the end are perserved.
            default: false

    - export
            Command line string to export the bookmarks. The string %mark
            is replaced with the mark and %path is replaced with the path.
            For example 'autojump --add %path' or 'zoxide add %path'.
            default: null

    - export_query
            Command line string to query if the bookmark is already
            exported. The string %mark is replaced with the mark and %path
            is replaced with the path. For example 'zoxide query %path'.
            default: null

    - mark
            Name of the bookmark.
            aliases: [bookmark]
            default: null

    - path
            Full path to the directory.
            aliases: [src]
            default: null

    - replace_home
            Replace home directory with $HOME variable.
            default: true

    - sdirs
            The path to the file where the bookmarks are stored.
            default: ~/.sdirs

    - sorted
            Sort entries in the bookmark file.
            default: true

    - state
            State of the mark.
            aliases: [src]
            choices: [present, absent]
            default: present

    AUTHOR: Josef Friedrich (@Josef-Friedrich)

    METADATA:
      metadata_version: '1.0'
      status:
      - preview
      supported_by: community

    EXAMPLES:

    # Bookmark the ansible configuration directory
    - shellmarks:
        mark: ansible
        path: /etc/ansible
        state: present

    # Delete bookmark of the ansible configuration directory
    - shellmarks:
        mark: ansible
        path: /etc/ansible
        state: absent

    # Replace home directory with $HOME variable
    - shellmarks:
        replace_home: true

    # Sort entries in the bookmark file
    - shellmarks:
        sorted: true

    # Delete bookmarks of no longer existing directories
    - shellmarks:
        cleanup: true

    RETURN VALUES:
    - changes
            A list of actions
            returned: On changed
            sample: [{action: add, mark: dir1, path: /dir1}, {action: delete, mark: dir1, path: /dir1},
              {action: sort, reverse: false, sort_by: mark}, {action: cleanup, count: 1}]
            type: list

Development
===========

Test functionality
------------------

::

   /usr/local/src/ansible/hacking/test-module -m shellmarks.py -a

Test documentation
------------------

::

   source /usr/local/src/ansible/hacking/env-setup
   /usr/local/src/ansible/test/sanity/validate-modules/validate-modules --arg-spec --warnings shellmarks.py

Generate documentation
----------------------

::

   ansible-doc -M . shellmarks
