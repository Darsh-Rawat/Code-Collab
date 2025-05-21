"use client"
import {
    Button,
    Field,
    Fieldset,
    For,
    Input,
    NativeSelect,
    Stack,
    AbsoluteCenter,
    Box,
    VStack,
    Link,
    Heading,
    Text,
    Tabs,
    InputGroup,
    Center,
    Flex,
    Grid,
    GridItem,
    Image,
    Separator,
    HStack,
    Checkbox,


} from "@chakra-ui/react"
import { PasswordInput, PasswordStrengthMeter, } from "@/components/ui/password-input"
import { RiArrowRightLine  } from "react-icons/ri";
import { CiMail } from "react-icons/ci";
import { useState } from "react"



const signin = () => {
    const [value, setValue] = useState("")
    return (
        <AbsoluteCenter>
            <VStack>
            <Image src={"/Under construction-bro.svg"} fit={"cover"} rounded="md" h={"md"} w={"md"}></Image>
            <Button asChild><a href="/auth/signin">Back<RiArrowRightLine size={"xs"} /></a></Button>
            </VStack>

        </AbsoluteCenter>

    )
}

export default signin

