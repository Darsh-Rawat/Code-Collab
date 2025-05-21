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
import { CiMail } from "react-icons/ci";
import { useState } from "react"



const signin = () => {
    const [value, setValue] = useState("")
    return (


        <Box
            position="absolute"
            top="50%"
            left="50%"
            transform="translate(-50%, -50%)"
            // bg={useColorModeValue("gray.100", "gray.800")}
            p={1}
            rounded="2xl"
            boxShadow="2xl"
        >
            <Grid
                templateColumns={{ base: "1fr", md: "1fr 1fr" }}
                maxW="800px"
                borderRadius="2xl"
                overflow="hidden"
            >
                {/* Left side image */}
                <GridItem display={{ base: "none", md: "block" }}>
                    <Image
                        src="/Login-amico.svg"
                        alt="Scenic"
                        objectFit="contain"
                        h="100%"
                        w="100%"
                    />
                </GridItem>

                {/* Right side form */}
                <GridItem
                    // bg={useColorModeValue("white", "gray.900")}
                    // color={useColorModeValue("gray.800", "white")}
                    p={8}
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                >
                    <Box w="full" maxW="md">
                        <Heading mb={2}>Sign In</Heading>
                        <Text mb={6} fontSize="sm" color="gray.500">
                            New here?{" "}
                            <Link href="/auth/signup" color="purple.400" >
                                Create Account
                            </Link>
                        </Text>

                        <Stack gap={4}>
                            {/* <Grid templateColumns="1fr 1fr" gap={4}>
                                <Input placeholder="First Name" />
                                <Input placeholder="Last Name" />
                            </Grid> */}
                            <Field.Root required>
                                <Field.Label>Email<Field.RequiredIndicator /></Field.Label>
                                <Input placeholder="Email" />
                            </Field.Root>
                            <Field.Root required>
                                <Field.Label>Passowrd<Field.RequiredIndicator /></Field.Label>
                                <PasswordInput placeholder="Password" value={value} onChange={(e) => setValue(e.target.value)}></PasswordInput>
                            </Field.Root>
                            {/* <PasswordStrengthMeter value={2} /> */}
                            <HStack gap={20}>
                                <Checkbox.Root>
                                    <Checkbox.HiddenInput />
                                    <Checkbox.Control />
                                    <Checkbox.Label>Remember Me</Checkbox.Label>
                                </Checkbox.Root>
                                <Link href="/auth/forgot-password" color="purple.400" >
                                    Forgot Password ?
                                </Link>

                            </HStack>

                            <Button colorScheme="purple" w="full">
                                Sign In
                            </Button>

                            <HStack>
                                <Separator flex="1" />
                                <Text textAlign="center" fontSize="sm" color="gray.500">
                                    Or
                                </Text>
                                <Separator flex="1" />
                            </HStack>

                            <Grid templateColumns="1fr 1fr" gap={4}>
                                <Button variant="outline">Google</Button>
                                <Button variant="outline">Apple</Button>
                            </Grid>
                        </Stack>
                    </Box>
                </GridItem>
            </Grid>
        </Box>

    )
}

export default signin

