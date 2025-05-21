"use client"
import { Box } from "@chakra-ui/react"

const NotFound = () => {
    return (
        <Box position="absolute"
            top="50%"
            left="50%"
            transform="translate(-50%, -50%)"
            bgImage={"/404 Error-amico.svg"}
            p={1}
            rounded="2xl"
            boxShadow="2xl"></Box>
    )
}

export default NotFound
