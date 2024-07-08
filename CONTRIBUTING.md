# Contributing to GWTrigFind

This page outlines the recommended procedure for contributing changes to the
GWTrigFind.
Please read the introduction to
[GitLab on git.ligo.org](https://computing.docs.ligo.org/guide/gitlab/)
before you start.

## Reporting Issues

Issues should be reported by opening a new ticket on the Gitlab project issue
tracker.

## Contributing code

All contributions must be made using the
[Project forking workflow](https://git.ligo.org/help/user/project/repository/forking_workflow.html).

If you wish to contribute new code, or changes to existing code,
please follow this development workflow:

### Make a fork (copy) of the project

**You only need to do this once**

1. Go to the [project home page](https://git.ligo.org/detchar/tools/gwtrigfind)
2. Click on the *Fork* button, that should lead you
   [here](https://git.ligo.org/detchar/tools/gwtrigfind/-/forks/new)
3. Select the namespace that you want to create the fork in, this will usually
   be your personal namespace

If you can't see the *Fork* button, make sure that you are logged in by
checking for your account profile photo in the top right-hand corner of
the screen.

### Clone your fork

Next, clone the main repo, calling it `upstream` in the git configuration:

```bash
git clone git@git.ligo.org:detchar/tools/gwtrigfind.git --origin upstream
```

and then add your fork as the `origin` remote (replace `<username>` with
your git.ligo.org username):

```bash
git remote add origin git@git.ligo.org:<username>/gwtrigfind.git
```

You can see which remotes are configured using

```bash
git remote -v
```

### Making changes

All changes should be developed on a feature branch in order to keep them
separate from other work, thus simplifying the review and merge once the
work is complete. The workflow is:

1. Create a new feature branch configured to track the `upstream/main` branch:

   ```bash
   git fetch upstream
   git checkout -b my-new-feature upstream/main
   ```

   This command creates the new branch `my-new-feature`, sets up tracking the
   `upstream` repository, and checks out the new branch.
   There are other ways to do these steps, but this is a good habit since it
   will allow you to `fetch` and `merge` changes from `upstream/main` directly
   onto the branch.

2. Develop the changes you would like to introduce, using `git commit` to
   finalise a specific change.
   Ideally commit small units of change often, rather than creating one large
   commit at the end, this will simplify review and make modifying any
   changes easier.

   Commit messages should be clear, identifying which code was changed,
   and why.
   Common practice is to use a short summary line (<50 characters),
   followed by a blank line, then more information in longer lines.

2. Push your changes to the remote copy of your fork on <https://git.ligo.org>.
   The first `push` of any new feature branch will require the
   `-u/--set-upstream` option to `push` to create a link between your new
   branch and the `origin` remote:

   ```bash
   git push --set-upstream origin my-new-feature
   ```

   Subsequent pushes can be made with just:

   ```bash
   git push
   ```

3. Keep your feature branch up to date with the `upstream` repository by doing:

   ```bash
   git pull --rebase upstream main
   git push --force origin my-new-feature
   ```

   If there are conflicts between `upstream` changes and your changes, you
   will need to resolve them before pushing everything to your fork. 

### Open a merge request

When you feel that your work is finished, you should create a merge request
to propose that your changes be merged into the main (`upstream`) repository.

After you have pushed your new feature branch to `origin`, you should find a
new button on the
[project home page](https://git.ligo.org/detchar/tools/gwtrigfind/)
inviting you to create a merge request out of your newly pushed branch.
(If the button does not exist, you can initiate a merge request by going to
the `Merge Requests` tab on your fork website on git.ligo.org and clicking
`New merge request`)

You should click the button, and proceed to fill in the title and description
boxes on the merge request page.
It is recommended that you check the box to `Remove source branch when merge
request is accepted`; this will result in the branch being automatically
removed from your fork when the merge request is accepted.

Once the request has been opened, one of the maintainers will assign someone
to review the change.
There may be suggestions and/or discussion with the reviewer.
These interactions are intended to make the resulting changes better.
The reviewer will merge your request.

Once the changes are merged into the upstream repository, you should remove
the development branch from your clone using

```bash
git branch -d my-new-feature
```

A feature branch should *not* be repurposed for further development as this
can result in problems merging upstream changes.

## More Information

More information regarding the usage of GitLab can be found in the main
GitLab [documentation](https://git.ligo.org/help/user/index.html).
