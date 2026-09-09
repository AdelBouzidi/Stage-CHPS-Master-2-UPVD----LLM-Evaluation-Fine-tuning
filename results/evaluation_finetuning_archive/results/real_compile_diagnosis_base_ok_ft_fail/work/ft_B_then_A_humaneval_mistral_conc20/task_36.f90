program fizz_buzz
  implicit none
  integer :: n, i, count, temp

  ! Read input n
  read(*, *) n

  count = 0
  do i = 1, n-1
    if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
      temp = i
      do while (temp /= 0)
        if (mod(temp, 10) == 7) then
          count = count + 1
        end if
        temp = temp / 10
      end do
    end if
  end do

  print *, count
end program fizz_buzz