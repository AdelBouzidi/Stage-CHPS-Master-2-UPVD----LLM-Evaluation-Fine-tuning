program fizz_buzz
  implicit none
  integer :: n
  integer :: count
  integer :: i
  integer :: temp

  ! Read input from stdin
  read(*,*) n

  ! Initialize count
  count = 0

  ! Loop through numbers less than n
  do i = 1, n-1
    if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
      temp = i
      do while (temp > 0)
        if (mod(temp, 10) == 7) then
          count = count + 1
        end if
        temp = temp / 10
      end do
    end if
  end do

  ! Output the result
  print *, count

end program fizz_buzz