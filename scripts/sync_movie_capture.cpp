// Observer only: finish the pending HD decode before Lua copies a screenshot.
// The 2.2.1 compiler inlines VideoDecoder::TakeScreenshot inside LuaApi, so
// intercept the public Lua callback and call the original callback unchanged.
#include "Shared/Emulator.h"
#include "Shared/Video/VideoDecoder.h"
#include <dlfcn.h>
#include <cstdlib>
#include <cstdio>
struct lua_State;
extern "C" int screenshot(lua_State*) asm("_ZN6LuaApi14TakeScreenshotEP9lua_State");
extern "C" int screenshot(lua_State* state){
 static void* core=dlopen(getenv("HOLY_DIVER_MESEN_CORE"),RTLD_NOW|RTLD_NOLOAD);
 static auto emulator=(Emulator**)dlsym(core,"_ZN6LuaApi4_emuE");
 static auto wait=(void(*)(void*))dlsym(core,"_ZN12VideoDecoder23WaitForAsyncFrameDecodeEv");
 static auto original=(int(*)(lua_State*))dlsym(core,"_ZN6LuaApi14TakeScreenshotEP9lua_State");
 if(!core||!emulator||!*emulator||!wait||!original)std::abort();
 static bool announced=false;
 if(!announced){announced=true;fprintf(stderr,"Synchronized native HD screenshot observer enabled.\n");}
 wait((*emulator)->GetVideoDecoder());return original(state);
}
