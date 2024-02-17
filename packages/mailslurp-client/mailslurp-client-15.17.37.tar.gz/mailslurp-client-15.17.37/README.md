# SDK Builder (CircleCI Packer Port)

This project takes runs entirely in CI and takes swagger inputs from MailSlurp (stored on s3) and generates clients
for many languages. 

It then runs bash scripts against the generated product to:

- add license and readme etc
- git tag and push
- upload artifact to package manager

See `.circleci/config.yml` for more.

## Deploy

- **Edit VERSION and then commit** (should be semver)
- Check circleci for status
