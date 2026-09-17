name: Test FDA RSS Access
 
# For now this only runs when you click the button manually.
# Once we confirm it works, we can add a "schedule:" section here
# so it also runs automatically on weekends.
on:
  workflow_dispatch:
 
jobs:
  test-access:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repo
        uses: actions/checkout@v4
 
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
 
      - name: Install dependencies
        run: pip install requests
 
      - name: Run FDA access test
        run: python test_fda_rss_access.py
 
