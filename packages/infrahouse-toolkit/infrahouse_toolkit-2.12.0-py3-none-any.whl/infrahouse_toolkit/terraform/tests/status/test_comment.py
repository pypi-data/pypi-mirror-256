from os import path as osp

import pytest

from infrahouse_toolkit.terraform.backends import TFS3Backend
from infrahouse_toolkit.terraform.status import RunOutput, RunResult, TFStatus


@pytest.mark.parametrize(
    "plan_file, result_counts, expected_comment",
    [
        (
            "plan-no-output.stdout",
            (1, 1, 1),
            """
# State **`s3://foo_backet/path/to/tf.state`**
## Affected resources counts

|  Success  |   🟢 Add |   🟡 Change |   🔴 Destroy |
|:---------:|--------:|-----------:|------------:|
|     ✅     |       1 |          1 |           1 |
<details>
<summary>STDOUT</summary>

```
no stdout
```
</details>
<details>
<summary>STDERR</summary>

```no output```
</details>
<details><summary><i>metadata</i></summary>
<p>
```eyJzMzovL2Zvb19iYWNrZXQvcGF0aC90by90Zi5zdGF0ZSI6IHsic3VjY2VzcyI6IHRydWUsICJzdGRvdXQiOiAibm8gc3Rkb3V0IiwgInN0ZGVyciI6IG51bGwsICJhZGQiOiAxLCAiY2hhbmdlIjogMSwgImRlc3Ryb3kiOiAxfX0=```
</p></details>""",
        ),
        (
            "plan-0-0-0.stdout",
            (0, 0, 0),
            """
# State **`s3://foo_backet/path/to/tf.state`**
## Affected resources counts

|  Success  |    Add |    Change |    Destroy |
|:---------:|-------:|----------:|-----------:|
|     ✅     |      0 |         0 |          0 |
<details>
<summary>STDOUT</summary>

```
Terraform has compared your real infrastructure against your configuration
and found no differences, so no changes are needed.
```
</details>
<details>
<summary>STDERR</summary>

```no output```
</details>
<details><summary><i>metadata</i></summary>
<p>
```eyJzMzovL2Zvb19iYWNrZXQvcGF0aC90by90Zi5zdGF0ZSI6IHsic3VjY2VzcyI6IHRydWUsICJzdGRvdXQiOiAiVGVycmFmb3JtIGhhcyBjb21wYXJlZCB5b3VyIHJlYWwgaW5mcmFzdHJ1Y3R1cmUgYWdhaW5zdCB5b3VyIGNvbmZpZ3VyYXRpb25cbmFuZCBmb3VuZCBubyBkaWZmZXJlbmNlcywgc28gbm8gY2hhbmdlcyBhcmUgbmVlZGVkLiIsICJzdGRlcnIiOiBudWxsLCAiYWRkIjogMCwgImNoYW5nZSI6IDAsICJkZXN0cm95IjogMH19```
</p></details>""",
        ),
        (
            "plan-2-0-0.stdout",
            (2, 0, 0),
            """
# State **`s3://foo_backet/path/to/tf.state`**
## Affected resources counts

|  Success  |   🟢 Add |    Change |    Destroy |
|:---------:|--------:|----------:|-----------:|
|     ✅     |       2 |         0 |          0 |
<details>
<summary>STDOUT</summary>

```
Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # module.repos["test"].github_repository.repo will be created
  + resource "github_repository" "repo" {
      + allow_auto_merge            = false
      + allow_merge_commit          = true
      + allow_rebase_merge          = true
      + allow_squash_merge          = true
      + archived                    = false
      + default_branch              = (known after apply)
      + delete_branch_on_merge      = false
      + description                 = "Template for a GitHub Control repository"
      + etag                        = (known after apply)
      + full_name                   = (known after apply)
      + git_clone_url               = (known after apply)
      + has_issues                  = true
      + html_url                    = (known after apply)
      + http_clone_url              = (known after apply)
      + id                          = (known after apply)
      + merge_commit_message        = "PR_TITLE"
      + merge_commit_title          = "MERGE_MESSAGE"
      + name                        = "test"
      + node_id                     = (known after apply)
      + private                     = (known after apply)
      + repo_id                     = (known after apply)
      + squash_merge_commit_message = "COMMIT_MESSAGES"
      + squash_merge_commit_title   = "COMMIT_OR_PR_TITLE"
      + ssh_clone_url               = (known after apply)
      + svn_url                     = (known after apply)
      + visibility                  = "public"

      + security_and_analysis {
          + advanced_security {
              + status = (known after apply)
            }

          + secret_scanning {
              + status = (known after apply)
            }

          + secret_scanning_push_protection {
              + status = (known after apply)
            }
        }
    }

  # module.repos["test"].github_team_repository.dev will be created
  + resource "github_team_repository" "dev" {
      + etag       = (known after apply)
      + id         = (known after apply)
      + permission = "push"
      + repository = "test"
      + team_id    = "7332815"
    }

Plan: 2 to add, 0 to change, 0 to destroy.

─────────────────────────────────────────────────────────────────────────────

Saved the plan to: tf.plan

To perform exactly these actions, run the following command to apply:
    terraform apply "tf.plan"
```
</details>
<details>
<summary>STDERR</summary>

```no output```
</details>
<details><summary><i>metadata</i></summary>
<p>
```eyJzMzovL2Zvb19iYWNrZXQvcGF0aC90by90Zi5zdGF0ZSI6IHsic3VjY2VzcyI6IHRydWUsICJzdGRvdXQiOiAiVGVycmFmb3JtIHVzZWQgdGhlIHNlbGVjdGVkIHByb3ZpZGVycyB0byBnZW5lcmF0ZSB0aGUgZm9sbG93aW5nIGV4ZWN1dGlvblxucGxhbi4gUmVzb3VyY2UgYWN0aW9ucyBhcmUgaW5kaWNhdGVkIHdpdGggdGhlIGZvbGxvd2luZyBzeW1ib2xzOlxuICArIGNyZWF0ZVxuXG5UZXJyYWZvcm0gd2lsbCBwZXJmb3JtIHRoZSBmb2xsb3dpbmcgYWN0aW9uczpcblxuICAjIG1vZHVsZS5yZXBvc1tcInRlc3RcIl0uZ2l0aHViX3JlcG9zaXRvcnkucmVwbyB3aWxsIGJlIGNyZWF0ZWRcbiAgKyByZXNvdXJjZSBcImdpdGh1Yl9yZXBvc2l0b3J5XCIgXCJyZXBvXCIge1xuICAgICAgKyBhbGxvd19hdXRvX21lcmdlICAgICAgICAgICAgPSBmYWxzZVxuICAgICAgKyBhbGxvd19tZXJnZV9jb21taXQgICAgICAgICAgPSB0cnVlXG4gICAgICArIGFsbG93X3JlYmFzZV9tZXJnZSAgICAgICAgICA9IHRydWVcbiAgICAgICsgYWxsb3dfc3F1YXNoX21lcmdlICAgICAgICAgID0gdHJ1ZVxuICAgICAgKyBhcmNoaXZlZCAgICAgICAgICAgICAgICAgICAgPSBmYWxzZVxuICAgICAgKyBkZWZhdWx0X2JyYW5jaCAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIGRlbGV0ZV9icmFuY2hfb25fbWVyZ2UgICAgICA9IGZhbHNlXG4gICAgICArIGRlc2NyaXB0aW9uICAgICAgICAgICAgICAgICA9IFwiVGVtcGxhdGUgZm9yIGEgR2l0SHViIENvbnRyb2wgcmVwb3NpdG9yeVwiXG4gICAgICArIGV0YWcgICAgICAgICAgICAgICAgICAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgZnVsbF9uYW1lICAgICAgICAgICAgICAgICAgID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgKyBnaXRfY2xvbmVfdXJsICAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIGhhc19pc3N1ZXMgICAgICAgICAgICAgICAgICA9IHRydWVcbiAgICAgICsgaHRtbF91cmwgICAgICAgICAgICAgICAgICAgID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgKyBodHRwX2Nsb25lX3VybCAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIGlkICAgICAgICAgICAgICAgICAgICAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgbWVyZ2VfY29tbWl0X21lc3NhZ2UgICAgICAgID0gXCJQUl9USVRMRVwiXG4gICAgICArIG1lcmdlX2NvbW1pdF90aXRsZSAgICAgICAgICA9IFwiTUVSR0VfTUVTU0FHRVwiXG4gICAgICArIG5hbWUgICAgICAgICAgICAgICAgICAgICAgICA9IFwidGVzdFwiXG4gICAgICArIG5vZGVfaWQgICAgICAgICAgICAgICAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgcHJpdmF0ZSAgICAgICAgICAgICAgICAgICAgID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgKyByZXBvX2lkICAgICAgICAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIHNxdWFzaF9tZXJnZV9jb21taXRfbWVzc2FnZSA9IFwiQ09NTUlUX01FU1NBR0VTXCJcbiAgICAgICsgc3F1YXNoX21lcmdlX2NvbW1pdF90aXRsZSAgID0gXCJDT01NSVRfT1JfUFJfVElUTEVcIlxuICAgICAgKyBzc2hfY2xvbmVfdXJsICAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIHN2bl91cmwgICAgICAgICAgICAgICAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgdmlzaWJpbGl0eSAgICAgICAgICAgICAgICAgID0gXCJwdWJsaWNcIlxuXG4gICAgICArIHNlY3VyaXR5X2FuZF9hbmFseXNpcyB7XG4gICAgICAgICAgKyBhZHZhbmNlZF9zZWN1cml0eSB7XG4gICAgICAgICAgICAgICsgc3RhdHVzID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgKyBzZWNyZXRfc2Nhbm5pbmcge1xuICAgICAgICAgICAgICArIHN0YXR1cyA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICsgc2VjcmV0X3NjYW5uaW5nX3B1c2hfcHJvdGVjdGlvbiB7XG4gICAgICAgICAgICAgICsgc3RhdHVzID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICMgbW9kdWxlLnJlcG9zW1widGVzdFwiXS5naXRodWJfdGVhbV9yZXBvc2l0b3J5LmRldiB3aWxsIGJlIGNyZWF0ZWRcbiAgKyByZXNvdXJjZSBcImdpdGh1Yl90ZWFtX3JlcG9zaXRvcnlcIiBcImRldlwiIHtcbiAgICAgICsgZXRhZyAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgaWQgICAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgcGVybWlzc2lvbiA9IFwicHVzaFwiXG4gICAgICArIHJlcG9zaXRvcnkgPSBcInRlc3RcIlxuICAgICAgKyB0ZWFtX2lkICAgID0gXCI3MzMyODE1XCJcbiAgICB9XG5cblBsYW46IDIgdG8gYWRkLCAwIHRvIGNoYW5nZSwgMCB0byBkZXN0cm95LlxuXG5cdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcdTI1MDBcblxuU2F2ZWQgdGhlIHBsYW4gdG86IHRmLnBsYW5cblxuVG8gcGVyZm9ybSBleGFjdGx5IHRoZXNlIGFjdGlvbnMsIHJ1biB0aGUgZm9sbG93aW5nIGNvbW1hbmQgdG8gYXBwbHk6XG4gICAgdGVycmFmb3JtIGFwcGx5IFwidGYucGxhblwiIiwgInN0ZGVyciI6IG51bGwsICJhZGQiOiAyLCAiY2hhbmdlIjogMCwgImRlc3Ryb3kiOiAwfX0=```
</p></details>""",
        ),
        (
            "plan-2-1-2.stdout",
            (2, 1, 2),
            """
# State **`s3://foo_backet/path/to/tf.state`**
## Affected resources counts

|  Success  |   🟢 Add |   🟡 Change |   🔴 Destroy |
|:---------:|--------:|-----------:|------------:|
|     ✅     |       2 |          1 |           2 |
<details>
<summary>STDOUT</summary>

```
Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create
  ~ update in-place
  - destroy

Terraform will perform the following actions:

  # module.repos["cookiecutter-github-control"].github_repository.repo will be destroyed
  # (because module.repos["cookiecutter-github-control"] is not in configuration)
  - resource "github_repository" "repo" {
      - allow_auto_merge            = false -> null
      - allow_merge_commit          = true -> null
      - allow_rebase_merge          = true -> null
      - allow_squash_merge          = true -> null
      - allow_update_branch         = false -> null
      - archived                    = false -> null
      - default_branch              = "main" -> null
      - delete_branch_on_merge      = false -> null
      - description                 = "Template for a GitHub Control repository" -> null
      - etag                        = "W/\\\"8b4a792bc1474d381caaa63b76668993b4adc42ae76ed53d6886d8562ebb0c67\\\"" -> null
      - full_name                   = "infrahouse/cookiecutter-github-control" -> null
      - git_clone_url               = "git://github.com/infrahouse/cookiecutter-github-control.git" -> null
      - has_discussions             = false -> null
      - has_downloads               = false -> null
      - has_issues                  = true -> null
      - has_projects                = false -> null
      - has_wiki                    = false -> null
      - html_url                    = "https://github.com/infrahouse/cookiecutter-github-control" -> null
      - http_clone_url              = "https://github.com/infrahouse/cookiecutter-github-control.git" -> null
      - id                          = "cookiecutter-github-control" -> null
      - is_template                 = false -> null
      - merge_commit_message        = "PR_TITLE" -> null
      - merge_commit_title          = "MERGE_MESSAGE" -> null
      - name                        = "cookiecutter-github-control" -> null
      - node_id                     = "R_kgDOI528zg" -> null
      - private                     = false -> null
      - repo_id                     = 597540046 -> null
      - squash_merge_commit_message = "COMMIT_MESSAGES" -> null
      - squash_merge_commit_title   = "COMMIT_OR_PR_TITLE" -> null
      - ssh_clone_url               = "git@github.com:infrahouse/cookiecutter-github-control.git" -> null
      - svn_url                     = "https://github.com/infrahouse/cookiecutter-github-control" -> null
      - topics                      = [] -> null
      - visibility                  = "public" -> null
      - vulnerability_alerts        = false -> null

      - security_and_analysis {

          - secret_scanning {
              - status = "disabled" -> null
            }

          - secret_scanning_push_protection {
              - status = "disabled" -> null
            }
        }
    }

  # module.repos["cookiecutter-github-control"].github_team_repository.dev will be destroyed
  # (because module.repos["cookiecutter-github-control"] is not in configuration)
  - resource "github_team_repository" "dev" {
      - etag       = "W/\\\"8043f81b19693f6c1a72d21bb8dc03859c98bf78bfbe79782bfe13fa813992ca\\\"" -> null
      - id         = "7332815:cookiecutter-github-control" -> null
      - permission = "push" -> null
      - repository = "cookiecutter-github-control" -> null
      - team_id    = "7332815" -> null
    }

  # module.repos["infrahouse-toolkit"].github_repository.repo will be updated in-place
  ~ resource "github_repository" "repo" {
      ~ description                 = "InfraHouse Toolkit" -> "InfraHouse Toolkit1"
        id                          = "infrahouse-toolkit"
        name                        = "infrahouse-toolkit"
        # (31 unchanged attributes hidden)

        # (1 unchanged block hidden)
    }

  # module.repos["test"].github_repository.repo will be created
  + resource "github_repository" "repo" {
      + allow_auto_merge            = false
      + allow_merge_commit          = true
      + allow_rebase_merge          = true
      + allow_squash_merge          = true
      + archived                    = false
      + default_branch              = (known after apply)
      + delete_branch_on_merge      = false
      + description                 = "Template for a GitHub Control repository"
      + etag                        = (known after apply)
      + full_name                   = (known after apply)
      + git_clone_url               = (known after apply)
      + has_issues                  = true
      + html_url                    = (known after apply)
      + http_clone_url              = (known after apply)
      + id                          = (known after apply)
      + merge_commit_message        = "PR_TITLE"
      + merge_commit_title          = "MERGE_MESSAGE"
      + name                        = "test"
      + node_id                     = (known after apply)
      + private                     = (known after apply)
      + repo_id                     = (known after apply)
      + squash_merge_commit_message = "COMMIT_MESSAGES"
      + squash_merge_commit_title   = "COMMIT_OR_PR_TITLE"
      + ssh_clone_url               = (known after apply)
      + svn_url                     = (known after apply)
      + visibility                  = "public"

      + security_and_analysis {
          + advanced_security {
              + status = (known after apply)
            }

          + secret_scanning {
              + status = (known after apply)
            }

          + secret_scanning_push_protection {
              + status = (known after apply)
            }
        }
    }

  # module.repos["test"].github_team_repository.dev will be created
  + resource "github_team_repository" "dev" {
      + etag       = (known after apply)
      + id         = (known after apply)
      + permission = "push"
      + repository = "test"
      + team_id    = "7332815"
    }

Plan: 2 to add, 1 to change, 2 to destroy.

─────────────────────────────────────────────────────────────────────────────

Saved the plan to: tf.plan

To perform exactly these actions, run the following command to apply:
    terraform apply "tf.plan"
```
</details>
<details>
<summary>STDERR</summary>

```no output```
</details>
<details><summary><i>metadata</i></summary>
<p>
```eyJzMzovL2Zvb19iYWNrZXQvcGF0aC90by90Zi5zdGF0ZSI6IHsic3VjY2VzcyI6IHRydWUsICJzdGRvdXQiOiAiVGVycmFmb3JtIHVzZWQgdGhlIHNlbGVjdGVkIHByb3ZpZGVycyB0byBnZW5lcmF0ZSB0aGUgZm9sbG93aW5nIGV4ZWN1dGlvblxucGxhbi4gUmVzb3VyY2UgYWN0aW9ucyBhcmUgaW5kaWNhdGVkIHdpdGggdGhlIGZvbGxvd2luZyBzeW1ib2xzOlxuICArIGNyZWF0ZVxuICB+IHVwZGF0ZSBpbi1wbGFjZVxuICAtIGRlc3Ryb3lcblxuVGVycmFmb3JtIHdpbGwgcGVyZm9ybSB0aGUgZm9sbG93aW5nIGFjdGlvbnM6XG5cbiAgIyBtb2R1bGUucmVwb3NbXCJjb29raWVjdXR0ZXItZ2l0aHViLWNvbnRyb2xcIl0uZ2l0aHViX3JlcG9zaXRvcnkucmVwbyB3aWxsIGJlIGRlc3Ryb3llZFxuICAjIChiZWNhdXNlIG1vZHVsZS5yZXBvc1tcImNvb2tpZWN1dHRlci1naXRodWItY29udHJvbFwiXSBpcyBub3QgaW4gY29uZmlndXJhdGlvbilcbiAgLSByZXNvdXJjZSBcImdpdGh1Yl9yZXBvc2l0b3J5XCIgXCJyZXBvXCIge1xuICAgICAgLSBhbGxvd19hdXRvX21lcmdlICAgICAgICAgICAgPSBmYWxzZSAtPiBudWxsXG4gICAgICAtIGFsbG93X21lcmdlX2NvbW1pdCAgICAgICAgICA9IHRydWUgLT4gbnVsbFxuICAgICAgLSBhbGxvd19yZWJhc2VfbWVyZ2UgICAgICAgICAgPSB0cnVlIC0+IG51bGxcbiAgICAgIC0gYWxsb3dfc3F1YXNoX21lcmdlICAgICAgICAgID0gdHJ1ZSAtPiBudWxsXG4gICAgICAtIGFsbG93X3VwZGF0ZV9icmFuY2ggICAgICAgICA9IGZhbHNlIC0+IG51bGxcbiAgICAgIC0gYXJjaGl2ZWQgICAgICAgICAgICAgICAgICAgID0gZmFsc2UgLT4gbnVsbFxuICAgICAgLSBkZWZhdWx0X2JyYW5jaCAgICAgICAgICAgICAgPSBcIm1haW5cIiAtPiBudWxsXG4gICAgICAtIGRlbGV0ZV9icmFuY2hfb25fbWVyZ2UgICAgICA9IGZhbHNlIC0+IG51bGxcbiAgICAgIC0gZGVzY3JpcHRpb24gICAgICAgICAgICAgICAgID0gXCJUZW1wbGF0ZSBmb3IgYSBHaXRIdWIgQ29udHJvbCByZXBvc2l0b3J5XCIgLT4gbnVsbFxuICAgICAgLSBldGFnICAgICAgICAgICAgICAgICAgICAgICAgPSBcIlcvXFxcIjhiNGE3OTJiYzE0NzRkMzgxY2FhYTYzYjc2NjY4OTkzYjRhZGM0MmFlNzZlZDUzZDY4ODZkODU2MmViYjBjNjdcXFwiXCIgLT4gbnVsbFxuICAgICAgLSBmdWxsX25hbWUgICAgICAgICAgICAgICAgICAgPSBcImluZnJhaG91c2UvY29va2llY3V0dGVyLWdpdGh1Yi1jb250cm9sXCIgLT4gbnVsbFxuICAgICAgLSBnaXRfY2xvbmVfdXJsICAgICAgICAgICAgICAgPSBcImdpdDovL2dpdGh1Yi5jb20vaW5mcmFob3VzZS9jb29raWVjdXR0ZXItZ2l0aHViLWNvbnRyb2wuZ2l0XCIgLT4gbnVsbFxuICAgICAgLSBoYXNfZGlzY3Vzc2lvbnMgICAgICAgICAgICAgPSBmYWxzZSAtPiBudWxsXG4gICAgICAtIGhhc19kb3dubG9hZHMgICAgICAgICAgICAgICA9IGZhbHNlIC0+IG51bGxcbiAgICAgIC0gaGFzX2lzc3VlcyAgICAgICAgICAgICAgICAgID0gdHJ1ZSAtPiBudWxsXG4gICAgICAtIGhhc19wcm9qZWN0cyAgICAgICAgICAgICAgICA9IGZhbHNlIC0+IG51bGxcbiAgICAgIC0gaGFzX3dpa2kgICAgICAgICAgICAgICAgICAgID0gZmFsc2UgLT4gbnVsbFxuICAgICAgLSBodG1sX3VybCAgICAgICAgICAgICAgICAgICAgPSBcImh0dHBzOi8vZ2l0aHViLmNvbS9pbmZyYWhvdXNlL2Nvb2tpZWN1dHRlci1naXRodWItY29udHJvbFwiIC0+IG51bGxcbiAgICAgIC0gaHR0cF9jbG9uZV91cmwgICAgICAgICAgICAgID0gXCJodHRwczovL2dpdGh1Yi5jb20vaW5mcmFob3VzZS9jb29raWVjdXR0ZXItZ2l0aHViLWNvbnRyb2wuZ2l0XCIgLT4gbnVsbFxuICAgICAgLSBpZCAgICAgICAgICAgICAgICAgICAgICAgICAgPSBcImNvb2tpZWN1dHRlci1naXRodWItY29udHJvbFwiIC0+IG51bGxcbiAgICAgIC0gaXNfdGVtcGxhdGUgICAgICAgICAgICAgICAgID0gZmFsc2UgLT4gbnVsbFxuICAgICAgLSBtZXJnZV9jb21taXRfbWVzc2FnZSAgICAgICAgPSBcIlBSX1RJVExFXCIgLT4gbnVsbFxuICAgICAgLSBtZXJnZV9jb21taXRfdGl0bGUgICAgICAgICAgPSBcIk1FUkdFX01FU1NBR0VcIiAtPiBudWxsXG4gICAgICAtIG5hbWUgICAgICAgICAgICAgICAgICAgICAgICA9IFwiY29va2llY3V0dGVyLWdpdGh1Yi1jb250cm9sXCIgLT4gbnVsbFxuICAgICAgLSBub2RlX2lkICAgICAgICAgICAgICAgICAgICAgPSBcIlJfa2dET0k1Mjh6Z1wiIC0+IG51bGxcbiAgICAgIC0gcHJpdmF0ZSAgICAgICAgICAgICAgICAgICAgID0gZmFsc2UgLT4gbnVsbFxuICAgICAgLSByZXBvX2lkICAgICAgICAgICAgICAgICAgICAgPSA1OTc1NDAwNDYgLT4gbnVsbFxuICAgICAgLSBzcXVhc2hfbWVyZ2VfY29tbWl0X21lc3NhZ2UgPSBcIkNPTU1JVF9NRVNTQUdFU1wiIC0+IG51bGxcbiAgICAgIC0gc3F1YXNoX21lcmdlX2NvbW1pdF90aXRsZSAgID0gXCJDT01NSVRfT1JfUFJfVElUTEVcIiAtPiBudWxsXG4gICAgICAtIHNzaF9jbG9uZV91cmwgICAgICAgICAgICAgICA9IFwiZ2l0QGdpdGh1Yi5jb206aW5mcmFob3VzZS9jb29raWVjdXR0ZXItZ2l0aHViLWNvbnRyb2wuZ2l0XCIgLT4gbnVsbFxuICAgICAgLSBzdm5fdXJsICAgICAgICAgICAgICAgICAgICAgPSBcImh0dHBzOi8vZ2l0aHViLmNvbS9pbmZyYWhvdXNlL2Nvb2tpZWN1dHRlci1naXRodWItY29udHJvbFwiIC0+IG51bGxcbiAgICAgIC0gdG9waWNzICAgICAgICAgICAgICAgICAgICAgID0gW10gLT4gbnVsbFxuICAgICAgLSB2aXNpYmlsaXR5ICAgICAgICAgICAgICAgICAgPSBcInB1YmxpY1wiIC0+IG51bGxcbiAgICAgIC0gdnVsbmVyYWJpbGl0eV9hbGVydHMgICAgICAgID0gZmFsc2UgLT4gbnVsbFxuXG4gICAgICAtIHNlY3VyaXR5X2FuZF9hbmFseXNpcyB7XG5cbiAgICAgICAgICAtIHNlY3JldF9zY2FubmluZyB7XG4gICAgICAgICAgICAgIC0gc3RhdHVzID0gXCJkaXNhYmxlZFwiIC0+IG51bGxcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgIC0gc2VjcmV0X3NjYW5uaW5nX3B1c2hfcHJvdGVjdGlvbiB7XG4gICAgICAgICAgICAgIC0gc3RhdHVzID0gXCJkaXNhYmxlZFwiIC0+IG51bGxcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cblxuICAjIG1vZHVsZS5yZXBvc1tcImNvb2tpZWN1dHRlci1naXRodWItY29udHJvbFwiXS5naXRodWJfdGVhbV9yZXBvc2l0b3J5LmRldiB3aWxsIGJlIGRlc3Ryb3llZFxuICAjIChiZWNhdXNlIG1vZHVsZS5yZXBvc1tcImNvb2tpZWN1dHRlci1naXRodWItY29udHJvbFwiXSBpcyBub3QgaW4gY29uZmlndXJhdGlvbilcbiAgLSByZXNvdXJjZSBcImdpdGh1Yl90ZWFtX3JlcG9zaXRvcnlcIiBcImRldlwiIHtcbiAgICAgIC0gZXRhZyAgICAgICA9IFwiVy9cXFwiODA0M2Y4MWIxOTY5M2Y2YzFhNzJkMjFiYjhkYzAzODU5Yzk4YmY3OGJmYmU3OTc4MmJmZTEzZmE4MTM5OTJjYVxcXCJcIiAtPiBudWxsXG4gICAgICAtIGlkICAgICAgICAgPSBcIjczMzI4MTU6Y29va2llY3V0dGVyLWdpdGh1Yi1jb250cm9sXCIgLT4gbnVsbFxuICAgICAgLSBwZXJtaXNzaW9uID0gXCJwdXNoXCIgLT4gbnVsbFxuICAgICAgLSByZXBvc2l0b3J5ID0gXCJjb29raWVjdXR0ZXItZ2l0aHViLWNvbnRyb2xcIiAtPiBudWxsXG4gICAgICAtIHRlYW1faWQgICAgPSBcIjczMzI4MTVcIiAtPiBudWxsXG4gICAgfVxuXG4gICMgbW9kdWxlLnJlcG9zW1wiaW5mcmFob3VzZS10b29sa2l0XCJdLmdpdGh1Yl9yZXBvc2l0b3J5LnJlcG8gd2lsbCBiZSB1cGRhdGVkIGluLXBsYWNlXG4gIH4gcmVzb3VyY2UgXCJnaXRodWJfcmVwb3NpdG9yeVwiIFwicmVwb1wiIHtcbiAgICAgIH4gZGVzY3JpcHRpb24gICAgICAgICAgICAgICAgID0gXCJJbmZyYUhvdXNlIFRvb2xraXRcIiAtPiBcIkluZnJhSG91c2UgVG9vbGtpdDFcIlxuICAgICAgICBpZCAgICAgICAgICAgICAgICAgICAgICAgICAgPSBcImluZnJhaG91c2UtdG9vbGtpdFwiXG4gICAgICAgIG5hbWUgICAgICAgICAgICAgICAgICAgICAgICA9IFwiaW5mcmFob3VzZS10b29sa2l0XCJcbiAgICAgICAgIyAoMzEgdW5jaGFuZ2VkIGF0dHJpYnV0ZXMgaGlkZGVuKVxuXG4gICAgICAgICMgKDEgdW5jaGFuZ2VkIGJsb2NrIGhpZGRlbilcbiAgICB9XG5cbiAgIyBtb2R1bGUucmVwb3NbXCJ0ZXN0XCJdLmdpdGh1Yl9yZXBvc2l0b3J5LnJlcG8gd2lsbCBiZSBjcmVhdGVkXG4gICsgcmVzb3VyY2UgXCJnaXRodWJfcmVwb3NpdG9yeVwiIFwicmVwb1wiIHtcbiAgICAgICsgYWxsb3dfYXV0b19tZXJnZSAgICAgICAgICAgID0gZmFsc2VcbiAgICAgICsgYWxsb3dfbWVyZ2VfY29tbWl0ICAgICAgICAgID0gdHJ1ZVxuICAgICAgKyBhbGxvd19yZWJhc2VfbWVyZ2UgICAgICAgICAgPSB0cnVlXG4gICAgICArIGFsbG93X3NxdWFzaF9tZXJnZSAgICAgICAgICA9IHRydWVcbiAgICAgICsgYXJjaGl2ZWQgICAgICAgICAgICAgICAgICAgID0gZmFsc2VcbiAgICAgICsgZGVmYXVsdF9icmFuY2ggICAgICAgICAgICAgID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgKyBkZWxldGVfYnJhbmNoX29uX21lcmdlICAgICAgPSBmYWxzZVxuICAgICAgKyBkZXNjcmlwdGlvbiAgICAgICAgICAgICAgICAgPSBcIlRlbXBsYXRlIGZvciBhIEdpdEh1YiBDb250cm9sIHJlcG9zaXRvcnlcIlxuICAgICAgKyBldGFnICAgICAgICAgICAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIGZ1bGxfbmFtZSAgICAgICAgICAgICAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgZ2l0X2Nsb25lX3VybCAgICAgICAgICAgICAgID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgKyBoYXNfaXNzdWVzICAgICAgICAgICAgICAgICAgPSB0cnVlXG4gICAgICArIGh0bWxfdXJsICAgICAgICAgICAgICAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgaHR0cF9jbG9uZV91cmwgICAgICAgICAgICAgID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgKyBpZCAgICAgICAgICAgICAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIG1lcmdlX2NvbW1pdF9tZXNzYWdlICAgICAgICA9IFwiUFJfVElUTEVcIlxuICAgICAgKyBtZXJnZV9jb21taXRfdGl0bGUgICAgICAgICAgPSBcIk1FUkdFX01FU1NBR0VcIlxuICAgICAgKyBuYW1lICAgICAgICAgICAgICAgICAgICAgICAgPSBcInRlc3RcIlxuICAgICAgKyBub2RlX2lkICAgICAgICAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIHByaXZhdGUgICAgICAgICAgICAgICAgICAgICA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICsgcmVwb19pZCAgICAgICAgICAgICAgICAgICAgID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgKyBzcXVhc2hfbWVyZ2VfY29tbWl0X21lc3NhZ2UgPSBcIkNPTU1JVF9NRVNTQUdFU1wiXG4gICAgICArIHNxdWFzaF9tZXJnZV9jb21taXRfdGl0bGUgICA9IFwiQ09NTUlUX09SX1BSX1RJVExFXCJcbiAgICAgICsgc3NoX2Nsb25lX3VybCAgICAgICAgICAgICAgID0gKGtub3duIGFmdGVyIGFwcGx5KVxuICAgICAgKyBzdm5fdXJsICAgICAgICAgICAgICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIHZpc2liaWxpdHkgICAgICAgICAgICAgICAgICA9IFwicHVibGljXCJcblxuICAgICAgKyBzZWN1cml0eV9hbmRfYW5hbHlzaXMge1xuICAgICAgICAgICsgYWR2YW5jZWRfc2VjdXJpdHkge1xuICAgICAgICAgICAgICArIHN0YXR1cyA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICsgc2VjcmV0X3NjYW5uaW5nIHtcbiAgICAgICAgICAgICAgKyBzdGF0dXMgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICArIHNlY3JldF9zY2FubmluZ19wdXNoX3Byb3RlY3Rpb24ge1xuICAgICAgICAgICAgICArIHN0YXR1cyA9IChrbm93biBhZnRlciBhcHBseSlcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cblxuICAjIG1vZHVsZS5yZXBvc1tcInRlc3RcIl0uZ2l0aHViX3RlYW1fcmVwb3NpdG9yeS5kZXYgd2lsbCBiZSBjcmVhdGVkXG4gICsgcmVzb3VyY2UgXCJnaXRodWJfdGVhbV9yZXBvc2l0b3J5XCIgXCJkZXZcIiB7XG4gICAgICArIGV0YWcgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIGlkICAgICAgICAgPSAoa25vd24gYWZ0ZXIgYXBwbHkpXG4gICAgICArIHBlcm1pc3Npb24gPSBcInB1c2hcIlxuICAgICAgKyByZXBvc2l0b3J5ID0gXCJ0ZXN0XCJcbiAgICAgICsgdGVhbV9pZCAgICA9IFwiNzMzMjgxNVwiXG4gICAgfVxuXG5QbGFuOiAyIHRvIGFkZCwgMSB0byBjaGFuZ2UsIDIgdG8gZGVzdHJveS5cblxuXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXHUyNTAwXG5cblNhdmVkIHRoZSBwbGFuIHRvOiB0Zi5wbGFuXG5cblRvIHBlcmZvcm0gZXhhY3RseSB0aGVzZSBhY3Rpb25zLCBydW4gdGhlIGZvbGxvd2luZyBjb21tYW5kIHRvIGFwcGx5OlxuICAgIHRlcnJhZm9ybSBhcHBseSBcInRmLnBsYW5cIiIsICJzdGRlcnIiOiBudWxsLCAiYWRkIjogMiwgImNoYW5nZSI6IDEsICJkZXN0cm95IjogMn19```
</p></details>""",
        ),
    ],
)
def test_comment(plan_file, result_counts, expected_comment):
    with open(osp.join("infrahouse_toolkit/terraform/tests/plans", plan_file)) as fp:
        status = TFStatus(
            TFS3Backend("foo_backet", "path/to/tf.state"), True, RunResult(*result_counts), RunOutput(fp.read(), None)
        )
        assert isinstance(status.comment, str)
        # print("\nActual comment:")
        # print(status.comment)
        # print("EOF Actual comment.")
        assert status.comment == expected_comment


def test_comment_none():
    status = TFStatus(
        TFS3Backend("foo_backet", "path/to/tf.state"),
        True,
        RunResult(None, None, None),
        RunOutput("no stdout", "no stderr"),
        affected_resources=RunResult(None, None, None),
    )
    assert isinstance(status.comment, str)
    print(status.comment)
