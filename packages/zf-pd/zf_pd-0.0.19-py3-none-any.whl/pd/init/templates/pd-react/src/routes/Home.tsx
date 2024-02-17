import {Flex, Image, Text} from "@chakra-ui/react";
import {Example} from "../apis/api";


export default function Home() {
    const data = Example()

    return (
        <Flex
            direction={"column"}
            fontFamily={"RosarioRegular, sans-serif"}
            margin={0}
            padding={0}
            width={"100%"}
            height={"100vh"}
            alignItems={"center"}
            justifyContent={"center"}
            textAlign={"center"}
        >
            <Text>
                {data["msg"] ? data["msg"] + " from " : "Welcome to"} <Text as={"span"} color={"blue"}>pd</Text>
            </Text>

            <Image src={"/img/pd.png"} alt={"pd"}/>

            <Text>
                Generated by pd © 2023. All Rights Reserved.
            </Text>
        </Flex>
    )
}