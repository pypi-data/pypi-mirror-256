#include <chrono>
#include <random>
#include <iostream>

#include "GraphInf/rng.h"
#include "GraphInf/types.h"


namespace GraphInf {

RNG rng;
size_t SEED=0;
void seed(size_t seed){ SEED=seed; rng.seed(seed); std::srand(seed); }
void seedWithTime(){
    seed(std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count());
}
const size_t& getSeed() { return SEED; }

}
