
#include "arb.hpp"
#include <iostream>
#include <nlohmann/json.hpp>
using json = nlohmann::json;
int main(){
    json in; std::cin >> in;
    std::vector<Quote> qs;
    for (auto& el: in){ qs.push_back(Quote{el["exchange"], el["bid"], el["ask"]}); }
    auto res = best_arbitrage(qs);
    if (!res){ std::cout << "{}\n"; return 0; }
    auto [buyEx, buyPx, sellEx, sellPx, bps] = *res;
    json out = { {"buy_exchange", buyEx}, {"buy_price", buyPx}, {"sell_exchange", sellEx}, {"sell_price", sellPx}, {"spread_bps", bps} };
    std::cout << out.dump() << "\n";
    return 0;
}
