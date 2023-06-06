import argparse
import sys
import os
import datetime
import subprocess
import time

def PlayAndWait(macro, timeout_seconds, var1='-', var2='-', var3='-', path_downloaddir=None, path_autorun_html=None, browser_path=None):
	
	assert os.path.exists(path_downloaddir)
	assert os.path.exists(path_autorun_html)
	# assert os.path.exists(browser_path)
	
	log = 'log_' + datetime.datetime.now().strftime('%m-%d-%Y_%H_%M_%S') + '.txt'
	
	path_log = os.path.join(path_downloaddir, log)
	
	args = r'file:///' + path_autorun_html + '?macro=' + macro + '&cmd_var1=' + var1 + '&cmd_var2=' + var2 + '&cmd_var3=' + var3 + '&closeRPA=0&direct=1&nodisplay=1&savelog=' + path_log
	
	proc = subprocess.Popen([browser_path, args])
	
	
	status_runtime = 0
	
	print("Log File will show up at " + path_log)

	timeout_seconds = int(timeout_seconds)
	while(not os.path.exists(path_log) and status_runtime < timeout_seconds):
		print("Waiting for macro to finish, seconds=%d" % status_runtime)
		time.sleep(1)
		status_runtime = status_runtime + 1
	
	if status_runtime < timeout_seconds:
		with open(path_log) as f:
			status_text = f.readline()
		
		status_init = 1 if status_text.find('Status=OK') != -1 else -1
	else:
		status_text = "Macro did not complete within the time given: %d" % timeout_seconds
		status_init = -2
		proc.kill()
	
	print(status_text)
	# sys.exit(status_init)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--path_downloaddir', required=True, help='Path to download directory')
	parser.add_argument('--path_autorun_html', required=True, help='Path to ui.vision.html file')
	parser.add_argument('--browser_path', required=True, help='Path to browser executable')
	parser.add_argument('--macro', required=True, help='UI.Vision RPA Macro name')
	parser.add_argument('-t', '--timeout', default=35, help='Timeout in seconds (default: 35)')
	parser.add_argument('--num_rows', required=True, help='The number of rows in the csv file+1')
	parser.add_argument('--var2', required=True, help='URL to Facebook Reels Composer page')
	parser.add_argument('--var3', required=True, help='Filename of the csv file')
	args = parser.parse_args()

	for x in range(1, int(args.num_rows)+1): # it will loop from 1 to args.num_rows but not args.num_rows+1
		var1 = str(x)
		# macro = "FB_Reels_CSV_API_Starter"
		PlayAndWait(macro=args.macro, timeout_seconds=args.timeout, var1=var1, var2=args.var2, var3=args.var3, path_downloaddir=args.path_downloaddir, path_autorun_html=args.path_autorun_html, browser_path=args.browser_path)