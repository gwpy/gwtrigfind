# Releasing `gwtrigfind`

The instructions below detail how to finalise a new release
for version `{X.Y.Z}`.

In all commands below that placeholder should be replaced
with an actual release version.

## 1. Create a tag/release on GitLab

1.  Draft release notes by looking through the merge requests associated
    with the relevant
    [milestone on GitLab](https://git.ligo.org/detchar/tools/gwtrigfind/-/milestones).

2.  Create a new Tag and Release using the GitLab UI.

    1.  Go to <https://git.ligo.org/detchar/tools/gwtrigfind/-/releases/new>

    2.  In the `Tag name` search box, enter the version number (`{X.Y.Z}`) as
        the new tag name and select `Create tag`.

    3.  In the message box, paste the release notes, then select `Save`.

    4.  For the `Release title`, please use `gwtrigfind {X.Y.Z}`.

    5.  In the `Milestones` dropdown menu box select the matching project
        milestone.

    6.  In the `Release notes` text box (for the `Release`), paste the release
        notes again. (This way the release notes are visible from both the `git`
        command-line client, _and_ the release page on the UI)

    7.  Under `Release Assets` add a link to the new tarball on PyPI. Use the
        following values:

        | Field | Value |
        | ----- | ----- |
        | URL | `https://pypi.io/packages/source/g/gwtrigfind/gwtrigfind-{X.Y.Z}.tar.gz` |
        | Link title | `Official source distribution` |
        | Type | `Package` |

The CI pipeline triggered by the creation of the git tag will automatically
build and upload a new source distribution and binary wheel to
<https://pypi.org/project/gwtrigfind>.

## 2. Open an SCCB request

To request approval for use of this new package for LVK research, please open
a new SCCB requests by going here:

<https://git.ligo.org/computing/sccb/-/issues/new>

Follow the instructions given in the issue template to include the details of
the new release.
Under `Details`, use the `https://pypi.io` URL format above for the `**Source:**`.
