program count_sevens
  implicit none
  integer :: n, i, count, num, digit
  integer :: result

  read *, n

  result = 0
  do i = 1, n - 1
    if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
      count = 0
      num = i
      do while (num > 0)
        digit = mod(num, 10)
        if (digit == 7) then
          count = count + 1
        end if
        num = num / 10
      end do
      result = result + count
    end if
  end do

  print *, result
end program count_sevens