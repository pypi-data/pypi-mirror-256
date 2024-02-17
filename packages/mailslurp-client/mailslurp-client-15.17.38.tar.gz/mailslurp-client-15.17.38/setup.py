from setuptools import setup, find_packages 

setup(
    name="mailslurp-client",
    version="15.17.38",
    description="Official MailSlurp Python SDK Email API",
    author="MailSlurp",
    author_email="contact@mailslurp.dev",
    url="https://www.mailslurp.com/python",
    keywords=["MailSlurp", "Email", "SMTP", "Mailer", "MailSlurp API", "Test"],
    install_requires=["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"],
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""
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
    """,
    long_description_content_type="text/markdown"
)
