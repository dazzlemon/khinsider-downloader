script_dir=$(dirname "$0")
file_path=$1
shift

PYTHONPATH="$PYTHONPATH:$script_dir/src" \
  scrapy runspider $script_dir/src/spider.py \
	-a file_path=$file_path \
	$@
