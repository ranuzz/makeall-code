#include <iostream>
#include <string>
#include "snippy.hpp"

std::string getOsName(void)
{
    #ifdef _WIN32 || _WIN64
        #ifdef _WIN64
        return "Windows 64-bit";
        #else
        return "Windows 32-bit";
        #endif
    #elif __APPLE__ || __MACH__
    return "Mac OSX";
    #elif __linux__
    return "Linux";
    #elif __FreeBSD__
    return "FreeBSD";
    #elif __unix || __unix__
    return "Unix";
    #else
    return "Other";
    #endif
}     

int main()
{
    std::cout << "Sample cpp project" << std::endl;
    std::string os = getOsName();
    std::cout << "Running on : " << os << std::endl;
}