"use client"
import { AbsoluteCenter, Box, VStack, Heading, Text, Separator, Stack, QrCode } from "@chakra-ui/react"
import { Clipboard, IconButton, Input, InputGroup } from "@chakra-ui/react"


const sharing = () => {
    return (
        <AbsoluteCenter>
            <Box bg={"gray.800"} w={"lg"} h={"md"} rounded={"xl"} >
                <Heading p={"3"} fontWeight={"extrabold"} fontFamily={"monospace"}>
                    Share And Collab
                </Heading>
                <Text p={"3"} pt={"0.5"} color={"gray.400"}>Your code is live share it with your friends.</Text>
                <Clipboard.Root p={"3"} maxW="500px" value="https://www.google.com">
                    <InputGroup bg={"gray.900"} endElement={<ClipboardIconButton />}>
                        <Clipboard.Input asChild>
                            <Input />
                        </Clipboard.Input>
                    </InputGroup>
                </Clipboard.Root>
                <AbsoluteCenter>
                    <Text fontWeight={"bold"} fontSize={"sm"} pt={"10%"} fontFamily={"monospace"} >Scan to Share</Text>
                </AbsoluteCenter>

                <AbsoluteCenter>

                    <QrCode.Root value="https://www.google.com" pt={"150%"}>
                        <QrCode.Frame>
                            <QrCode.Pattern />
                        </QrCode.Frame>
                    </QrCode.Root>
                </AbsoluteCenter>

                <AbsoluteCenter>
                    <Text pt={"270%"} color={"gray.400"} fontWeight={"bold"} fontFamily={"monospace"} >Scan using Phone.</Text>
                </AbsoluteCenter>

            </Box>
        </AbsoluteCenter>
    )
}


const ClipboardIconButton = () => {
    return (
        <Clipboard.Trigger asChild>
            <IconButton variant="surface" size="xs" me="-2">
                <Clipboard.Indicator />
            </IconButton>
        </Clipboard.Trigger>
    )
}

export default sharing
