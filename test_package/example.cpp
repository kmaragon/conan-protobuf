#include <iostream>
#include "test.pb.h"

int main() 
{
    test::conan::pbuftest::TestMessage msg;
    msg.set_message_id("Test00001");
    msg.set_timestamp(time(NULL));    

    std::string data;
    msg.SerializeToString(&data);

    std::cout << "Serialized data: ";
    std::cout.flush();
    for (size_t i = 0; i < data.size(); i++)
        printf("%.2X", data[i]);
    std::cout << std::endl;
    return 0;
}
