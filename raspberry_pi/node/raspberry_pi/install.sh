pushd .
cp -r ../raspberry_pi/ $SDRROOT/dev/nodes
cd $SDRROOT/dev/nodes/raspberry_pi
./clone_node.py
popd
