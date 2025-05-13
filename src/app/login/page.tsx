"use client"

import { Button, For, HStack, useToastStyles } from "@chakra-ui/react"
import { toaster } from "@/components/ui/toaster"


const page = () => {

  return (
 <HStack>
      <For each={["success", "error", "warning", "info"]}>
        {(type) => (
          <Button
            size="sm"
            variant="outline"
            key={type}
            onClick={() =>
              toaster.create({
                title: `Toast status is ${type}`,
                type: type,
              })
            }
          >
            {type}
          </Button>
        )}
      </For>
    </HStack>
  )
}

export default page
