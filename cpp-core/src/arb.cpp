
#include "arb.hpp"
#include <limits>
std::optional<std::tuple<std::string,double,std::string,double,double>>
best_arbitrage(const std::vector<Quote>& qs){
    if (qs.empty()) return std::nullopt;
    double bestBid=-std::numeric_limits<double>::infinity(); std::string sellEx;
    double bestAsk= std::numeric_limits<double>::infinity(); std::string buyEx;
    for (auto& q: qs){ if (q.bid > bestBid){ bestBid=q.bid; sellEx=q.exchange; }
                        if (q.ask < bestAsk){ bestAsk=q.ask; buyEx=q.exchange; } }
    if (sellEx == buyEx) return std::nullopt;
    double bps = (bestBid - bestAsk)/bestAsk*1e4;
    if (bps > 5.0) return std::make_tuple(buyEx, bestAsk, sellEx, bestBid, bps);
    return std::nullopt;
}
