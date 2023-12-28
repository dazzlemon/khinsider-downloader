script_dir=$(dirname "$0")
start_url=$1
shift

PYTHONPATH="$PYTHONPATH:$script_dir/src" \
  scrapy runspider $script_dir/src/spider.py \
	-a start_url=$start_url \
	$@
