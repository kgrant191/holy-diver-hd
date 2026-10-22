// Test harness only: enable Mesen's own WAV recorder at the first audio buffer.
// The original mixer receives the same arguments, unchanged.
#include <dlfcn.h>
#include <cstdlib>
#include <cstdint>
#include <string>
#include <cstdio>
extern "C" void mix(void*,int16_t*,uint32_t,uint32_t)
  asm("_ZN10SoundMixer15PlayAudioBufferEPsjj");
extern "C" void mix(void* self,int16_t* samples,uint32_t count,uint32_t rate) {
  static void* core=dlopen(getenv("HOLY_DIVER_MESEN_CORE"),RTLD_NOW|RTLD_NOLOAD);
  static auto original=(void(*)(void*,int16_t*,uint32_t,uint32_t))dlsym(core,"_ZN10SoundMixer15PlayAudioBufferEPsjj");
  if(!core || !original) { fprintf(stderr,"Set HOLY_DIVER_MESEN_CORE to MesenCore.so's absolute path.\n"); std::abort(); }
  static bool started=false;
  if(!started) {
    started=true;
    const char* path=getenv("HOLY_DIVER_AUDIO_CAPTURE");
    if(path) {
      auto start=(void(*)(void*,std::string))dlsym(core,"_ZN10SoundMixer14StartRecordingENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE");
      start(self,std::string(path));
      fprintf(stderr,"Mesen WAV capture: %s at source rate %u\n",path,rate);
    }
  }
  original(self,samples,count,rate);
}
