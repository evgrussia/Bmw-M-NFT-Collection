pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract BmwMCollection is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    enum Models{I4, IX, M2, M3, M4_CABRIO, M4_CSL, M5, M8_CABRIO, M8_COUPE, M235, M760, M850, X5M, X6M, X7M, XM, Z4}

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Models) public tokenIdToModel;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event RequestedCollectible(bytes32 indexed requestId); 

    event ReturnedCollectible(bytes32 indexed requestId, uint256 randomNumber);


    bytes32 internal keyHash;
    uint256 internal fee;
    
    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash)
    public 
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Bmw M Collection", "MKA")
    {
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18;
    }

    function createCollectible(string memory tokenURI) 
        public returns (bytes32){
            bytes32 requestId = requestRandomness(keyHash, fee);
            requestIdToSender[requestId] = msg.sender;
            requestIdToTokenURI[requestId] = tokenURI;
            emit RequestedCollectible(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        address bmwOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(bmwOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);
        Models model = Models(randomNumber % 17);
        tokenIdToModel[newItemId] = model;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
        emit ReturnedCollectible(requestId, randomNumber);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
