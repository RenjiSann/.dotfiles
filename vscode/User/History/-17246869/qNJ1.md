# Qarnot PFEE CI

This project is meant to develop a working POC for GitLab CI using code coverage

The actual test project is an fnmatch implementation exposed in a static
library (this is a third year EPITA project, implementation is the one of
Dorian Péron).

The GitLab CI should do all these things:

- Install all the testing environment
- Build the library **with coverage flags**
- Compile the test suite **without coverage flags**
- Run the tests
- Collect Gcov Information
- Use Gcovr to get:
  - the coverage %age.
  - the coverage data in Cobertura format
  - the coverage data in HTML format
- Expose all the coverage data to artifacts for the GitLab interface


### Notes on GitLab interface:

#### Enable pipeline widget for merge requests
This shows the coverage percentage in the merge request
with a little toast:
![](imgs/mr_pipeline.png)

If not working, go to `https://<gitlab_url>/<project_path>/-/settings/merge_requests` and enable this:
![](imgs/mr_pipeline_setting.png)

#### Limitations
**About coverage visualisation in the MR diffs**:
the downside is that the files that are untouched in by
the merge request are not displayed, so you can't know
the evolution of their coverage.
This is particularly problematic if your MR just adds tests
for example, because their impact on the source code coverage is not seen.