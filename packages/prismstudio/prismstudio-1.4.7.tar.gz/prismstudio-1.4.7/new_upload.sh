export ENV_STATE=$1
export VERSION=$2

echo "ENV_STATE=$ENV_STATE"$'\n'"VERSION=$VERSION" > prismstudio/_common/.env

python -m build

# twine upload dist/* -u __token__ -p $token


# PS_FILES="/home/prism/miniconda3/envs/prism/conda-bld/linux-64/prismstudio-*"
# rm $PS_FILES
# conda activate prism
# conda build conda-receipe --no-test
# for f in $PS_FILES
# do
#     echo "Processing $f file..."
#     conda convert -f --platform all $f -o dist/
# done

# ARCH=( "win-64" "osx-arm64" "linux-aarch64" )
# for ar in "${ARCH[@]}"
# do
#     FILES="dist/$ar/*"
#     for f in $FILES
#     do
#         echo "Uploading $f ..."
#         anaconda upload $f
#     done
# done