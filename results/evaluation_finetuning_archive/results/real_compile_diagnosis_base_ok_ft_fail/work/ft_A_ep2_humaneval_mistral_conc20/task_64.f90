program vowels_count
  implicit none
  character(len=5) :: input = 'abcde'
  integer :: result

  result = vowels_count(input)
  print *, result

contains

  integer function vowels_count(s)
    character(len=*), intent(in) :: s
    integer :: i, len_s
    character(len=1) :: ch

    len_s = len_trim(s)
    vowels_count = 0

    do i = 1, len_s
      ch = s(i:i)
      select case (ichar(ch))
      case (97, 101, 105, 111, 117)
        vowels_count = vowels_count + 1
      case (65, 69, 73, 79, 85)
        vowels_count = vowels_count + 1
      case (121)
        if (i == len_s) then
          vowels_count = vowels_count + 1
        end if
      case (89)
        if (i == len_s) then
          vowels_count = vowels_count + 1
        end if
      end select
    end do

  end function vowels_count

end program vowels_count