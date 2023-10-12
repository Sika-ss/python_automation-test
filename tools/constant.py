import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

conf_test_dir = os.path.join(root_dir, 'config', 'conf_test.cfg')

conf_uat_dir = os.path.join(root_dir, 'config', 'conf_uat.cfg')

conf_prod_dir = os.path.join(root_dir, 'config', 'conf_prod.cfg')

globe_conf_dir = os.path.join(root_dir, 'config', 'conf_globe.cfg')

report_dir = os.path.join(root_dir, 'output', 'report')

data_dir = os.path.join(root_dir, 'data')

log_dir = os.path.join(root_dir, 'log')

case_data_dir = os.path.join(root_dir, "case_data")

