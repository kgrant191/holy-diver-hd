// Diagnostic observer for stock Mesen 2.2.1. Abort before the known one-past-
// screen tileNearby read. Forward every valid call unchanged. Never ship this.
#include "NES/HdPacks/HdPackConditions.h"
#include <dlfcn.h>
#include <cstdlib>
#include <cstdio>
#include <unordered_map>
#include <unordered_set>

using Check = bool(*)(HdPackBaseTileCondition*, int, int, HdPpuTileInfo*);
static std::unordered_map<void**, Check> originalChecks;
static std::unordered_map<void**, void**> patchedTables;
struct ScreenAccessor : HdPackTileNearbyCondition {
    static uint32_t Frame(HdPackBaseTileCondition* p) {
        return static_cast<ScreenAccessor*>(p)->_screenInfo->FrameNumber;
    }
};
static bool check(HdPackBaseTileCondition* self, int x, int y, HdPpuTileInfo* tile) {
    int index = self->PixelOffset + y*256 + x;
    if(index == NesConstants::ScreenPixelCount) {
        fprintf(stderr, "HD_NEIGHBOR_ONE_PAST_END name=%s frame=%u x=%d y=%d dx=%d dy=%d index=%d tile=%04X\n",
            self->Name.c_str(), ScreenAccessor::Frame(self), x, y,
            self->TileX, self->TileY, index, tile ? tile->TileIndex : -1);
        fflush(stderr);
        std::abort();
    }
    return originalChecks.at(*reinterpret_cast<void***>(self))(self,x,y,tile);
}
extern "C" void process(void*, std::vector<std::string>&, std::vector<HdPackCondition*>)
 asm("_ZN12HdPackLoader14ProcessTileTagERSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS6_EES0_IP15HdPackConditionSaISB_EE");
extern "C" void process(void* self, std::vector<std::string>& tokens, std::vector<HdPackCondition*> conditions) {
    static void* core=dlopen(getenv("HOLY_DIVER_MESEN_CORE"),RTLD_NOW|RTLD_NOLOAD);
    using Process = void(*)(void*,std::vector<std::string>&,std::vector<HdPackCondition*>);
    static auto original=reinterpret_cast<Process>(dlsym(core,
        "_ZN12HdPackLoader14ProcessTileTagERSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS6_EES0_IP15HdPackConditionSaISB_EE"));
    if(!core || !original) std::abort();
    for(auto* condition:conditions) {
        if(condition->GetConditionType()!=HdPackConditionType::TileNearby) continue;
        auto& table=*reinterpret_cast<void***>(condition);
        if(originalChecks.count(table)) continue;
        if(!patchedTables.count(table)) {
            auto* storage=new void*[9];
            std::copy(table-2,table+7,storage);
            auto* replacement=storage+2;
            originalChecks[replacement]=reinterpret_cast<Check>(table[6]);
            replacement[6]=reinterpret_cast<void*>(&check);
            patchedTables[table]=replacement;
        }
        table=patchedTables.at(table);
    }
    original(self,tokens,conditions);
}
