# flag technique from Jon Almeida: https://jonalmeida.com/posts/2013/05/26/different-ways-to-implement-flags-in-bash/

while [ ! $# -eq 0 ]
do
	case "$1" in
		--hairline | -h)
			source $(dirname ${BASH_SOURCE[0]})/build-hairline/build-hairline.sh
			;;
		--final | -f)
			source $(dirname ${BASH_SOURCE[0]})/build-final/build-final.sh
			;;
		--all | -a)
			source $(dirname ${BASH_SOURCE[0]})/build-hairline/build-hairline.sh
			source $(dirname ${BASH_SOURCE[0]})/build-final/build-final.sh
			;;
	esac
	shift
done