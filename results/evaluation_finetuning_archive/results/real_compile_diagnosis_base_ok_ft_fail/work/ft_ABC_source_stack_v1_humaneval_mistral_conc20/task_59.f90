program main
  implicit none
  integer :: n, i, largest
  integer :: temp

  ! Read input
  read *, n

  ! Find largest prime factor
  largest = 2
  temp = n

  ! Check for factor 2
  if (mod(temp, 2) == 0) then
    largest = 2
    do while (mod(temp, 2) == 0)
      temp = temp / 2
    end do
  end if

  ! Check for odd factors
  i = 3
  do while (i * i <= temp)
    if (mod(temp, i) == 0) then
      largest = i
      do while (mod(temp, i) == 0)
        temp = temp / i
      end do
    end if
    i = i + 2
  end do

  ! If temp > 1, then it's a prime factor
  if (temp > 1) then
    largest = temp
  end if

  ! Output result
  print *, largest
end program main