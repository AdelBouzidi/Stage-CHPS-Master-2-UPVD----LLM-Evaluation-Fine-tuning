program even_odd_palindrome
  implicit none
  integer :: n
  integer :: even_count, odd_count
  integer :: i
  integer :: temp
  integer :: reversed
  integer :: digit
  integer :: power_of_10

  ! Read input
  read(*,*) n

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Check each number from 1 to n
  do i = 1, n
    temp = i
    reversed = 0
    power_of_10 = 1
    
    ! Reverse the number
    do while (temp > 0)
      digit = mod(temp, 10)
      reversed = reversed + digit * power_of_10
      temp = temp / 10
      power_of_10 = power_of_10 * 10
    end do
    
    ! Check if palindrome
    if (i == reversed) then
      if (mod(i, 2) == 0) then
        even_count = even_count + 1
      else
        odd_count = odd_count + 1
      end if
    end if
  end do

  ! Output results
  print *, even_count, odd_count

end program even_odd_palindrome