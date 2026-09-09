program vowels_count
  implicit none
  character(len=*), dimension(1) :: input
  integer :: i, count
  character(len=1) :: c

  ! Read input
  read *, input

  ! Count vowels
  count = 0
  do i = 1, size(input)
    c = input(i)
    if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
        c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
      count = count + 1
    else if (c == 'y' .or. c == 'Y') then
      ! y is a vowel only at the end of the word
      if (i == size(input)) then
        count = count + 1
      end if
    end if
  end do

  ! Output result
  print *, count

end program vowels_count