#!/usr/bin/python
# -*- coding: utf-8 -*-

# Porting from main.py in this directory
# Gnnng <gnnnnng@gmail.com>

import os

from argparse import ArgumentParser
import list_white
import list_ip

def parse_args():
	parser = ArgumentParser()
	parser.add_argument('-i', '--input', dest='input', default=os.path.join('data','me.qusic.skia.js'),
		help='path to skia config template')
	parser.add_argument('-o', '--output', dest='output', default='me.qusic.skia.js',
		help='path to output skia config', metavar='SKIA')
	parser.add_argument('-p', '--proxy', dest='proxy', default='"127.0.0.1:10090"',
		help='the proxy parameter in the skia file, for example,\
		"127.0.0.1:10090;"', metavar='SOCKS5')
	return parser.parse_args()

def get_file_data(filename):
	content = ''
	with open(filename, 'r') as file_obj:
		content = file_obj.read()
	return content

def writefile(input_file, proxy, output_file):
	# Not used
	# ip_content = list_ip.final_list()
	# ip16_content = list_ip.center_list()
	# fake_ip_content = list_ip.fake_list()
	domains_content = list_white.final_list()
	proxy_content = get_file_data(input_file)
	proxy_host, proxy_ip = proxy.strip('"').split(":")

	proxy_content = proxy_content.replace('__PROXY_HOST__', proxy_host)
	proxy_content = proxy_content.replace('__PROXY_PORT__', proxy_ip)
	proxy_content = proxy_content.replace('__DOMAINS__', domains_content)
	# Not used
	# proxy_content = proxy_content.replace('__IP_LIST__', ip_content)
	# proxy_content = proxy_content.replace('__IP16_LIST__', ip16_content)
	# proxy_content = proxy_content.replace('__FAKE_IP_LIST__', fake_ip_content)
	with open(output_file, 'w') as file_obj:
		file_obj.write(proxy_content)

def main():
	args = parse_args()
	writefile(args.input, '"' + args.proxy.strip('"') + '"', args.output)

if __name__ == '__main__':
	main()

