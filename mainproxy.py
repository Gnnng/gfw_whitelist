#!/usr/bin/python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import re
import list_white
import list_black
import list_gfw
import list_ip

def parse_args():
	parser = ArgumentParser()
	parser.add_argument('-i', '--input', dest='input', default='data\\proxy.pac',
		help='path to gfwlist')
	parser.add_argument('-o', '--output', dest='output', default='proxy.pac',
		help='path to output pac', metavar='PAC')
	parser.add_argument('-p', '--proxy', dest='proxy', default='"SOCKS5 127.0.0.1:1080;"',
		help='the proxy parameter in the pac file, for example,\
		"127.0.0.1:1080;"', metavar='SOCKS5')
	parser.add_argument('-a', '--auto_proxy', dest='auto_proxy', default='"SOCKS5 127.0.0.1:1080;"',
		help='the auto proxy parameter in the pac file, for example,\
		"127.0.0.1:1080;"', metavar='SOCKS5')
	parser.add_argument('-d', '--dynamic', dest='dynamic', default='no')
	return parser.parse_args()

def get_file_data(filename):
	content = ''
	with open(filename, 'r') as file_obj:
		content = file_obj.read()
	return content

def js_shorter(content):
	r = re.compile(r'; \/\/.*')
	content = r.sub(';', content)
	#content = content.replace('\n', ' ')
	content = content.replace('\t', '')
	return content

def writefile(input_file, proxy, auto_proxy, output_file, dynamic):
	ip_content = list_ip.final_list()
	ip16_content = list_ip.center_list()
	proxy_content = get_file_data(input_file)
	proxy_content = proxy_content.replace('__IP_LIST__', ip_content)
	proxy_content = proxy_content.replace('__IP16_LIST__', ip16_content)
	proxy_content = proxy_content.replace('__FAKE_IP_LIST__', list_ip.fake_list())
	proxy_content = proxy_content.replace('__WHITE_DOMAINS__', list_white.final_list())
	if '__BLACK_DOMAINS__' in proxy_content:
		proxy_content = proxy_content.replace('__BLACK_DOMAINS__', list_black.final_list())
	if '__GFWBLACK_DOMAINS__' in proxy_content:
		proxy_content = proxy_content.replace('__GFWBLACK_DOMAINS__', list_gfw.final_list())

	if dynamic != 'no':
		with open(dynamic + output_file, 'w') as file_obj:
			file_obj.write( js_shorter(proxy_content) )

	proxy_content = proxy_content.replace('__PROXY__', proxy)
	proxy_content = proxy_content.replace('__NOWALL_PROXY__', '"DIRECT;"')
	proxy_content = proxy_content.replace('__AUTO_PROXY__', auto_proxy)
	proxy_content = proxy_content.replace('__DIRECT__', '"DIRECT;"')
	with open(output_file, 'w') as file_obj:
		file_obj.write(proxy_content)

	with open('min_' + output_file, 'w') as file_obj:
		file_obj.write(js_shorter(proxy_content))

def main():
	args = parse_args()
	writefile(args.input, '"' + args.proxy.strip('"') + '"', '"' + args.auto_proxy.strip('"') + '"', args.output, args.dynamic)

if __name__ == '__main__':
	main()

