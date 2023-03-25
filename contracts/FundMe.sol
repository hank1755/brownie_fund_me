// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract FundMe is Ownable {
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) Ownable() {
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * 10 ** 18;
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "Min value $50 ETH"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // ETH/USD rate in 18 digit
        return uint256(answer * 10000000000); //answer variable from contract interface is the price
    }

    function getConversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountinUSD = (ethPrice * ethAmount) / 1000000000000000000; //divide by the wei to convert
        return ethAmountinUSD;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        // set mappings of funder amount funded to 0
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0); // reset funders array to 0 once all balances have been reset to 0
    }
}
