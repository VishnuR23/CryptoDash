
#pragma once
#include <string>
#include <vector>
#include <tuple>
#include <optional>
struct Quote { std::string exchange; double bid; double ask; };
std::optional<std::tuple<std::string,double,std::string,double,double>> best_arbitrage(const std::vector<Quote>& qs);
