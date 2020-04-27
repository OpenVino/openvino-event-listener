pragma solidity >=0.4.22 <=0.6.0;

contract RootRecord {

    mapping (bytes32 => bool) private roots;
    event InsertedRoot(bytes32 indexed _root);
    
    function addRoot(bytes32 _root) public {
        roots[_root] = true;
        emit InsertedRoot(_root);
    }

    function getRoot(bytes32 _root) public view returns (bool) {
        return roots[_root];
    }

}
