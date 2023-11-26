@echo off

IF "%~1" "=" "L" (
  irtools "sendir" "--raw=+9092 -4403 +638 -456 +639 -456 +638 -456 +639 -456 +638 -456 +635 -456 +638 -456 +639 -456 +638 -1589 +638 -1585 +638 -1589 +638 -1584 +643 -1585 +638 -1584 +617 -1610 +639 -1584 +642 -452 +643 -1584 +638 -456 +639 -1584 +642 -1585 +638 -456 +613 -1610 +643 -451 +643 -1584 +638 -456 +639 -1588 +639 -451 +643 -452 +617 -1610 +639 -456 +638 -1584 +643" "--repeat=1"
) ELSE (
  IF "%~1" "=" "A" (
    irtools "sendir" "--raw=+9067 -4426 +638 -456 +639 -456 +639 -456 +639 -456 +639 -456 +634 -461 +634 -461 +634 -456 +639 -1589 +664 -1559 +639 -1588 +639 -1585 +638 -1589 +639 -1584 +638 -1589 +638 -1588 +665 -426 +642 -456 +639 -1584 +638 -456 +639 -456 +649 -445 +639 -1588 +665 -430 +635 -1588 +639 -1584 +643 -456 +639 -1584 +613 -1614 +638 -1584 +613 -482 +638 -1588 +665" "--repeat=1"
  ) ELSE (
    IF "%~1" "=" "B" (
      irtools "sendir" "--raw=+9092 -4402 +639 -456 +638 -456 +638 -456 +639 -456 +638 -456 +638 -456 +613 -482 +638 -452 +668 -1559 +612 -1611 +668 -1559 +639 -1584 +669 -1558 +639 -1589 +638 -1601 +626 -1584 +638 -1589 +664 -1558 +643 -1585 +638 -457 +638 -456 +639 -452 +643 -452 +643 -451 +643 -452 +638 -456 +639 -456 +639 -1584 +643 -1584 +639 -1588 +639 -1584 +639 -1589 +639" "--repeat=1"
    ) ELSE (
      IF "%~1" "=" "C" (
        irtools "sendir" "--raw=+9093 -4403 +638 -457 +638 -456 +639 -456 +639 -456 +634 -461 +634 -460 +635 -460 +635 -456 +639 -1589 +612 -1611 +639 -1589 +613 -1611 +638 -1590 +638 -1585 +638 -1589 +639 -1584 +613 -1615 +638 -456 +639 -456 +613 -1610 +643 -452 +639 -456 +639 -456 +639 -456 +639 -456 +613 -1610 +639 -1589 +665 -430 +613 -1610 +638 -1589 +639 -1585 +643 -1585 +639" "--repeat=1"
      ) ELSE (
        IF "%~1" "=" "D" (
          irtools "sendir" "--raw=+9062 -4433 +613 -482 +608 -482 +639 -456 +638 -456 +638 -456 +639 -456 +638 -456 +639 -456 +613 -1610 +638 -1589 +638 -1585 +638 -1601 +626 -1584 +643 -1584 +642 -1585 +639 -1584 +643 -454 +636 -456 +638 -456 +639 -456 +638 -456 +639 -456 +612 -1610 +639 -456 +639 -1588 +639 -1584 +613 -1614 +638 -1584 +643 -1583 +639 -1588 +638 -456 +639 -1584 +639" "--repeat=1"
        ) ELSE (
          IF "%~1" "=" "E" (
            irtools "sendir" "--raw=+9066 -4430 +639 -456 +639 -456 +613 -482 +608 -487 +634 -461 +634 -456 +639 -456 +639 -456 +639 -1584 +613 -1615 +613 -1610 +639 -1589 +639 -1592 +631 -1589 +638 -1585 +638 -1589 +639 -1584 +639 -456 +613 -482 +639 -1584 +639 -1589 +639 -456 +639 -456 +634 -456 +639 -456 +639 -1589 +613 -1610 +639 -456 +639 -456 +639 -1585 +638 -1589 +639 -1584 +639" "--repeat=1"
          ) ELSE (
            IF "%~1" "=" "F" (
              irtools "sendir" "--raw=+9092 -4402 +638 -456 +639 -451 +643 -452 +643 -451 +669 -426 +643 -451 +643 -452 +643 -451 +639 -1588 +639 -1584 +643 -1584 +639 -1584 +643 -1584 +639 -1585 +668 -1559 +643 -1584 +665 -430 +638 -1585 +668 -1559 +642 -452 +639 -1584 +642 -452 +643 -452 +642 -452 +643 -1584 +643 -451 +643 -452 +664 -1559 +643 -451 +643 -1585 +643 -1580 +668 -1559 +668" "--repeat=1"
            ) ELSE (
              IF "%~1" "=" "G" (
                irtools "sendir" "--raw=+9071 -4425 +638 -456 +639 -456 +639 -451 +644 -451 +643 -452 +643 -452 +639 -456 +638 -456 +639 -1584 +643 -1584 +643 -1579 +643 -1584 +643 -1585 +638 -1585 +643 -1584 +639 -1584 +643 -452 +643 -451 +639 -1584 +643 -1584 +643 -452 +639 -456 +664 -430 +639 -452 +643 -1584 +639 -1584 +643 -452 +643 -451 +643 -1585 +638 -1584 +669 -1559 +638 -1585 +643" "--repeat=1"
              ) ELSE (
                IF "%~1" "=" "H" (
                  irtools "sendir" "--raw=+9097 -4399 +643 -452 +639 -456 +638 -456 +639 -452 +669 -426 +643 -451 +639 -456 +639 -456 +639 -1585 +643 -1584 +639 -1584 +643 -1584 +639 -1584 +643 -1584 +643 -1585 +639 -1584 +643 -452 +617 -478 +639 -456 +638 -1585 +643 -1584 +639 -456 +639 -451 +643 -452 +643 -1585 +638 -1585 +643 -1584 +639 -452 +643 -451 +643 -1585 +643 -1580 +643 -1584 +639" "--repeat=1"
                ) ELSE (
                  IF "%~1" "=" "I" (
                    irtools "sendir" "--raw=+9096 -4398 +643 -452 +642 -452 +643 -452 +643 -451 +643 -452 +639 -456 +638 -456 +639 -456 +664 -1558 +643 -1584 +639 -1588 +639 -1584 +669 -1558 +638 -1584 +669 -1559 +616 -1610 +639 -456 +638 -1584 +669 -1558 +643 -1584 +638 -1584 +643 -452 +668 -1558 +643 -452 +642 -1584 +639 -456 +664 -430 +639 -456 +638 -452 +668 -1558 +643 -452 +669 -1558 +638" "--repeat=1"
                  ) ELSE (
                    IF "%~1" "=" "J" (
                      irtools "sendir" "--raw=+9068 -4428 +640 -452 +639 -456 +643 -452 +639 -456 +638 -457 +638 -452 +643 -452 +639 -456 +639 -1589 +639 -1584 +617 -1611 +639 -1584 +639 -1589 +639 -1585 +617 -1611 +639 -1585 +638 -457 +639 -456 +639 -456 +665 -1558 +643 -452 +639 -456 +639 -456 +638 -457 +647 -1576 +643 -1585 +639 -1584 +643 -452 +643 -1586 +637 -1584 +643 -1584 +643 -1585 +639" "--repeat=1"
                    ) ELSE (
                      IF "%~1" "=" "U" (
                        irtools "sendir" "--raw=+9070 -4425 +643 -452 +641 -453 +639 -456 +639 -456 +664 -426 +643 -455 +639 -452 +643 -451 +639 -1589 +638 -1584 +639 -1584 +643 -1585 +638 -1589 +664 -1559 +638 -1584 +643 -1585 +638 -456 +639 -456 +638 -1585 +643 -1584 +639 -1584 +643 -452 +638 -456 +639 -456 +639 -1584 +643 -1584 +655 -436 +668 -426 +643 -452 +643 -1602 +621 -1584 +643 -1585 +638" "--repeat=1"
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
)