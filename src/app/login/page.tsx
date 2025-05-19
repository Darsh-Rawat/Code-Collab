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
} from "@chakra-ui/react"
import { PasswordInput } from "@/components/ui/password-input"
import { useState } from "react"



const page = () => {
    const [value, setValue] = useState("")
    return (
        <Box minH="100vh"
            backgroundImage="url('/img.png')"
            backgroundSize="cover"
            backgroundPosition="center"
            backgroundRepeat="no-repeat">
            <AbsoluteCenter bg={"gray.50"} rounded={"2xl"} boxSize={"md"} p={8} boxShadow={"md"}>
                <Fieldset.Root size="lg" maxW="md">

                    <Fieldset.Content>


                        <Field.Root>
                            <Field.Label color={"#262d36"} fontWeight={"semibold"} fontSize={"md"} fontFamily={"body"} >Email address</Field.Label>
                            <Input name="email" type="email" variant={"outline"}  css={{ "--focus-color": "colors.blue.400" }} bg={"white"} color={"black"} w={"sm"} />
                        </Field.Root>


                        <Field.Root>
                            <Field.Label color={"#262d36"} fontWeight={"semibold"} fontSize={"md"} fontFamily={"body"}>Password</Field.Label>
                            <PasswordInput  css={{ "--focus-color": "colors.blue.400" }} bg={"white"} color={"black"} value={value} onChange={(e) => setValue(e.target.value)} />
                        </Field.Root>

                    </Fieldset.Content>

                    <Button type="submit" alignSelf="stretch" bg={"blue.400"} _hover={{ bg: "blue.500" }} color={"white"} fontWeight={"bolder"}>
                        Sign in
                    </Button>
                </Fieldset.Root>
            </AbsoluteCenter>
        </Box>

    )
}

export default page

