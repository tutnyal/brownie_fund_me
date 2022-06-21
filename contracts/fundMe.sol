//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMeContrc {
    mapping(address => uint256) public AddressToFunds;

    address owner;
    address[] public funders;
    AggregatorV3Interface priceFeed;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fundMe() public payable {
        uint256 minFunding = 50 * 10**18; //$50 for min fudning amount
        require(
            convertEth_USD(msg.value) >= minFunding,
            "Funding must be more than $50"
        );
        AddressToFunds[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(
        //     address(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e)
        // );
        return priceFeed.version();
    }

    function getUSDPrice() public view returns (uint256) {
        // AggregatorV3Interface USDPrice = AggregatorV3Interface(
        //     address(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e)
        // );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
        //Why does the price come in x10^8, shouldnt it be gwei which is x10^9?
    }

    function convertEth_USD(uint256 _EthPrice) public view returns (uint256) {
        uint256 EthPrice = getUSDPrice();
        uint256 ethAmountUSD = (EthPrice * _EthPrice) / 1000000000000000000;
        return ethAmountUSD;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getUSDPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }

    modifier onlyOwner() {
        require(owner == msg.sender, "You must be owner to withdraw the funds");
        _;
    }

    function withdrawFunds() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 _index = 0; _index < funders.length; _index++) {
            address funder = funders[_index];
            AddressToFunds[funder] = 0;
        }
        funders = new address[](0);
    }
}
